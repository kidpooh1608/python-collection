#!/usr/bin/python3
import requests
import os
import bs4
from tqdm import tqdm
import urllib.request

class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize

class common:
    @staticmethod
    def dowload(url, filename):
        print("dowloading " + url)
        #eg_link = "https://caspersci.uk.to/matryoshka.zip"
        with TqdmUpTo(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:  # all optional kwargs
            urllib.request.urlretrieve(url, filename=filename, reporthook=t.update_to, data=None)

url = 'http://xkcd.com'

os.makedirs('xkcd', exist_ok=True)

for i in range (1, 10, 1):
    print('Downloading page...{0}'.format(url))
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features="html.parser")
    commicElem = soup.select("#comic img")

    if commicElem == []:
        print('Could not find comic image')
    else:
        comicURL = 'http:' + commicElem[0].get('src')
        print('Downloading image...{0}'.format(comicURL))
        common.dowload(comicURL, os.path.basename(comicURL))

        # res = requests.get(comicURL)
        # res.raise_for_status()

        # imageFile = open(os.path.join('xkcd', os.path.basename(comicURL)), 'wb')
        # for chunk in res.iter_content(100000):
        #     imageFile.write(chunk)
        # imageFile.close()

    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')

print('Done')
