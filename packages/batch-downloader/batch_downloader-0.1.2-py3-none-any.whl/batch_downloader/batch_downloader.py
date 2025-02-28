"""
批量下载器，支持单个文件和分块下载。
"""

import os
from typing import Callable, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

from batch_downloader.base_downloader import BaseDownloader

class BatchDownloader(BaseDownloader):
    """
    批量下载器，支持单个文件和分块下载，并增加断点续传功能。
    """
    def __init__(
        self,
        urls: List[str],
        output_dir: str = "downloads",
        chunk_size: int = 8192,
        max_workers: int = 8,
        progress_callback: Optional[Callable[[str, int, int], None]] = None,
    ):
        super().__init__(urls, output_dir, chunk_size, progress_callback)
        self.max_workers = max_workers

    def download_file(
        self,
        url: str,
        output_filename: Optional[str] = None,
    ) -> str:
        """
        下载单个文件，支持自定义输出文件名和断点续传。
        """
        local_filename = self.get_local_filename(url, output_filename)

        # 检查文件是否已部分下载
        if os.path.exists(local_filename):
            downloaded_size = os.path.getsize(local_filename)
        else:
            downloaded_size = 0

        headers = {}
        if downloaded_size > 0:
            headers["Range"] = f"bytes={downloaded_size}-"

        with requests.get(url, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0)) + downloaded_size

            # 以追加模式打开文件
            with open(local_filename, 'ab') as f:
                for chunk in r.iter_content(chunk_size=self.chunk_size):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    self.update_progress(url, downloaded_size, total_size)

        return local_filename

    def download_file_chunked(
        self,
        url: str,
        output_filename: Optional[str] = None,
    ) -> str:
        """
        对单个文件实行分块下载，加快下载速度，并支持断点续传。
        """
        local_filename = self.get_local_filename(url, output_filename)

        # 获取文件总大小
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))

        # 定义分块下载函数
        def download_chunk(start: int, end: int, chunk_id: int) -> None:
            part_filename = f"{local_filename}.part{chunk_id}"
            if os.path.exists(part_filename):
                downloaded_size = os.path.getsize(part_filename)
                if downloaded_size == end - start + 1:
                    return  # 该分块已经下载完成
                start += downloaded_size

            headers = {"Range": f"bytes={start}-{end}"}
            with requests.get(url, headers=headers, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(part_filename, 'ab') as f:
                    for chunk in r.iter_content(chunk_size=self.chunk_size):
                        f.write(chunk)

        # 计算每个块的大小
        chunk_size = total_size // self.max_workers
        ranges = [
            (i * chunk_size, (i + 1) * chunk_size - 1 if i < self.max_workers - 1 else total_size - 1)
            for i in range(self.max_workers)
        ]

        # 使用线程池下载分块
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(download_chunk, start, end, i)
                for i, (start, end) in enumerate(ranges)
            ]
            for future in as_completed(futures):
                future.result()

        # 合并分块文件
        with open(local_filename, 'wb') as f:
            for i in range(self.max_workers):
                part_filename = f"{local_filename}.part{i}"
                with open(part_filename, 'rb') as part_file:
                    f.write(part_file.read())
                os.remove(part_filename)

        # 更新进度
        self.update_progress(url, total_size, total_size)

        return local_filename

    def download_all(
        self,
        output_filenames: Optional[List[str]] = None,
        chunked: bool = False,
    ) -> List[str]:
        """
        下载所有文件，支持自定义输出文件名和分块下载，并支持断点续传。
        """
        if output_filenames is None:
            output_filenames = [None] * len(self.urls)

        downloaded_files = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(
                    self.download_file_chunked if chunked else self.download_file,
                    url,
                    output_filename,
                )
                for url, output_filename in zip(self.urls, output_filenames)
            ]
            for future in as_completed(futures):
                try:
                    downloaded_files.append(future.result())
                except Exception as e:
                    raise e

        return downloaded_files