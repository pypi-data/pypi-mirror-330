import os
from typing import Callable, List, Optional

class BaseDownloader:
    def __init__(
        self,
        urls: List[str],
        output_dir: str = "downloads",
        chunk_size: int = 8192,
        progress_callback: Optional[Callable[[str, int, int], None]] = None,
    ):
        self.urls = urls
        self.output_dir = output_dir
        self.chunk_size = chunk_size
        self.progress_callback = progress_callback
        os.makedirs(self.output_dir, exist_ok=True)

    def get_local_filename(self, url: str, output_filename: Optional[str]) -> str:
        """
        根据 URL 和自定义文件名生成本地文件名。
        """
        if output_filename is None:
            output_filename = url.split('/')[-1]
        return os.path.join(self.output_dir, output_filename)

    def update_progress(self, url: str, downloaded_size: int, total_size: int) -> None:
        """
        更新下载进度。
        """
        if self.progress_callback:
            self.progress_callback(url, downloaded_size, total_size)