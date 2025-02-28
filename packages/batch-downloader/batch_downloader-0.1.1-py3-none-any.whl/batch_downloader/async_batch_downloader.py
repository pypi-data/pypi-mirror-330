"""
异步批量下载器，支持分块下载。
"""

import os
from typing import Callable, List, Optional
import asyncio
import aiohttp
from batch_downloader.base_downloader import BaseDownloader

class AsyncBatchDownloader(BaseDownloader):
    """
    异步批量下载器，支持分块下载。
    """
    def __init__(
        self,
        urls: List[str],
        output_dir: str = "downloads",
        chunk_size: int = 8192,
        progress_callback: Optional[Callable[[str, int, int], None]] = None,
        max_concurrent_downloads: int = 10  # 控制并发下载数量
    ):
        super().__init__(urls, output_dir, chunk_size, progress_callback)
        self.semaphore = asyncio.Semaphore(max_concurrent_downloads)

    async def download_chunk(
        self,
        session: aiohttp.ClientSession,
        url: str,
        start: int,
        end: int,
        temp_filename: str,
        progress_queue: asyncio.Queue  # 用于传递下载进度
    ) -> None:
        """下载文件的一个分块，并更新进度"""
        headers = {'Range': f'bytes={start}-{end}'}
        
        async with self.semaphore:  # 控制并发数量
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                with open(temp_filename, 'r+b') as f:
                    f.seek(start)
                    async for chunk in response.content.iter_chunked(self.chunk_size):
                        f.write(chunk)
                        await progress_queue.put(len(chunk))  # 将下载的字节数放入队列

    async def download_file(
        self,
        session: aiohttp.ClientSession,
        url: str,
        output_filename: Optional[str] = None,
        num_chunks: int = 4  # 分块数量可配置
    ) -> str:
        """
        异步分块下载单个文件，支持自定义输出文件名和进度更新。
        """
        local_filename = self.get_local_filename(url, output_filename)
        temp_filename = local_filename + '.tmp'

        # 获取文件总大小
        async with session.head(url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

        if total_size == 0:
            # 如果无法获取文件大小，fallback 到普通下载
            return await self._simple_download(session, url, local_filename)

        # 创建临时文件并分配空间
        with open(temp_filename, 'wb') as f:
            f.truncate(total_size)

        # 计算每个分块的大小
        chunk_size = total_size // num_chunks
        tasks = []
        progress_queue = asyncio.Queue()  # 用于跟踪下载进度

        # 创建下载任务
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size - 1 if i < num_chunks - 1 else total_size - 1
            tasks.append(
                self.download_chunk(session, url, start, end, temp_filename, progress_queue)
            )

        # 启动进度更新任务
        progress_task = asyncio.create_task(self._update_progress_from_queue(
            url, total_size, progress_queue
        ))

        # 执行所有分块下载任务
        await asyncio.gather(*tasks)

        # 等待进度更新任务完成
        await progress_queue.join()
        progress_task.cancel()

        # 下载完成后重命名文件
        os.rename(temp_filename, local_filename)
        return local_filename

    async def _update_progress_from_queue(
        self,
        url: str,
        total_size: int,
        progress_queue: asyncio.Queue
    ) -> None:
        """从队列中获取下载进度并更新"""
        downloaded_size = 0
        while True:
            chunk_size = await progress_queue.get()
            downloaded_size += chunk_size
            self.update_progress(url, downloaded_size, total_size)
            progress_queue.task_done()

    async def _simple_download(
        self,
        session: aiohttp.ClientSession,
        url: str,
        local_filename: str
    ) -> str:
        """当无法分块时的备用下载方法"""
        async with session.get(url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            with open(local_filename, 'wb') as f:
                async for chunk in response.content.iter_chunked(self.chunk_size):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    self.update_progress(url, downloaded_size, total_size)
        return local_filename

    async def download_all(
        self,
        output_filenames: Optional[List[str]] = None,
        num_chunks_per_file: int = 4
    ) -> List[str]:
        """
        异步下载所有文件，支持分块下载和自定义输出文件名。
        """
        if output_filenames is None:
            output_filenames = [None] * len(self.urls)

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.download_file(session, url, output_filename, num_chunks_per_file)
                for url, output_filename in zip(self.urls, output_filenames)
            ]
            return await asyncio.gather(*tasks)