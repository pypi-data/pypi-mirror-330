import ssl
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_bs(url, allow_unverified=False):
    try:
        if allow_unverified:
            with urlopen(
                url, context=ssl._create_unverified_context()
            ) as response:
                html = response.read().decode()
        else:
            html = urlopen(url).read()
    except HTTPError as e:
        print(e)
        return None
    except URLError:
        print("The server could not be found!")
        return None
    else:
        bs = BeautifulSoup(html, "html.parser")
        return bs
