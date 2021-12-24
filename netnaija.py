#! python3

import requests


def download_movie(url):
    filename = "sub.zip"
    r = requests.get(url)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(100000):
            f.write(chunk)
    print("downloaded")


download_movie(
    "https://subscene.com/subtitles/english-text/6sQTPdyda0x-X8R4eVioFIhRpI1K1SDguBW71yce504mg6dYhgvn6KGUhQB_fCDVPgD55KDmqUUNJ2kb48aGcENuZOnpY0158Z6nEaxCAktm8k3o7ViFbdQk1Uybj1TO0"
)
