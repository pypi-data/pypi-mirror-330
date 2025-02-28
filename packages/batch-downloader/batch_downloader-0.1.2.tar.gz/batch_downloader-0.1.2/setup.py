from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="batch_downloader",
    version="0.1.2",
    author="zhenpingzhan",
    author_email="stallzhan@gmail.com",
    description="A simple batch downloader with chunked downloads",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/Zzhenping/batch_downloader",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "aiohttp>=3.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)