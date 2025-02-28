# Batch Downloader

A simple Python package for downloading multiple files in parallel with chunked downloads.

## Installation

```bash
pip install batch_downloader
```

## Usage

```python
def progress_callback(url: str, downloaded_size: int, total_size: int):
    if total_size > 0:
        progress = (downloaded_size / total_size) * 100
        print(f"Downloading {url}: {progress:.2f}%")
    else:
        print(f"Downloading {url}: {downloaded_size} bytes (total size unknown)")

downloader = BatchDownloader(
    urls=[
        "xxx",
        "xxx",
        ],
    output_dir="downloads",
    progress_callback=progress_callback,
)

results = downloader.download_all()
```

## Async Usage

```python

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
```




