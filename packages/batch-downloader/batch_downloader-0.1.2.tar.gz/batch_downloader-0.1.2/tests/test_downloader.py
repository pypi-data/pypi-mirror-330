import time
from batch_downloader import BatchDownloader

s = time.time()
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

# 下载文件并显示进度
results = downloader.download_all()
print(f"Downloaded files: {results}")
print(f"Total time: {time.time() - s:.2f} seconds")