import asyncio
import unittest
from batch_downloader.async_batch_downloader import AsyncBatchDownloader

class TestAsyncBatchDownloader(unittest.TestCase):

    def progress_callback(self, url: str, downloaded_size: int, total_size: int):
        if total_size > 0:
            progress = (downloaded_size / total_size) * 100
            print(f"Downloading {url.split('/')[-1]}: {progress:.2f}% ({downloaded_size}/{total_size} bytes)")
        else:
            print(f"Downloading {url.split('/')[-1]}: {downloaded_size} bytes (total size unknown)")

    async def async_test_download(self):
        downloader = AsyncBatchDownloader(
            urls=[
                "xxx",
                "xxx",
            ],
            output_dir="downloads",
            progress_callback=self.progress_callback,
        )
        results = await downloader.download_all()
        self.assertTrue(isinstance(results, list))

    def test_download(self):
        asyncio.run(self.async_test_download())

if __name__ == "__main__":
    unittest.main()