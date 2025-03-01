from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

from heliodash.packages.util.html_video import mpg_to_html5video


def stereo_video(
    products=[],
):
    root_dir = Path("./data")
    root_dir.mkdir(exist_ok=True)

    product_information = {
        "A_171": r"STEREO-A EUVI 171 Å",
        "A_195": r"STEREO-A EUVI 195 Å",
        "A_284": r"STEREO-A EUVI 284 Å",
        "A_304": r"STEREO-A EUVI 304 Å",
        "A_COR1": r"STEREO-A COR1",
        "A_COR2": r"STEREO-A COR2",
        "B_171": r"STEREO-B EUVI 171 Å",
        "B_195": r"STEREO-B EUVI 195 Å",
        "B_284": r"STEREO-B EUVI 284 Å",
        "B_304": r"STEREO-B EUVI 304 Å",
        "B_COR1": r"STEREO-B COR1",
        "B_COR2": r"STEREO-B COR2",
    }

    # https://stereo-ssc.nascom.nasa.gov/browse/2025/02/17/ahead_20250217_euvi_195_512.mpg
    # https://stereo-ssc.nascom.nasa.gov/browse/2014/01/01/behind_20140101_euvi_195_512.mpg
    # https://stereo-ssc.nascom.nasa.gov/browse/2014/01/01/behind_20140101_cor1_512.mpg

    # latest available videos
    obstime = datetime.now(timezone.utc)

    root = "https://stereo-ssc.nascom.nasa.gov/browse/"

    p2prefix = {
        "A_171": "ahead_",
        "A_195": "ahead_",
        "A_284": "ahead_",
        "A_304": "ahead_",
        "A_COR1": "ahead_",
        "A_COR2": "ahead_",
        "B_171": "behind_",
        "B_195": "behind_",
        "B_284": "behind_",
        "B_304": "behind_",
        "B_COR1": "behind_",
        "B_COR2": "behind_",
    }

    p2suffix = {
        "A_171": "_euvi_171_512.mpg",
        "A_195": "_euvi_195_512.mpg",
        "A_284": "_euvi_284_512.mpg",
        "A_304": "_euvi_304_512.mpg",
        "A_COR1": "_cor1_512.mpg",
        "A_COR2": "_cor2_512.mpg",
        "B_171": "_euvi_171_512.mpg",
        "B_195": "_euvi_195_512.mpg",
        "B_284": "_euvi_284_512.mpg",
        "B_304": "_euvi_304_512.mpg",
        "B_COR1": "_cor1_512.mpg",
        "B_COR2": "_cor2_512.mpg",
    }

    time = deepcopy(obstime)
    info = {}
    for p in products:
        if p not in product_information:
            continue
        if p[0] == "B":
            time = datetime(2014, 10, 1, 0, 0, 0, 0, timezone.utc)
            # https://stereo-ssc.nascom.nasa.gov/behind_status.shtml
            # Communications with STEREO-B were lost on Oct. 1, 2014
        url = (
            root
            + time.strftime("%Y/%m/%d/")
            + p2prefix[p]
            + time.strftime("%Y%m%d")
            + p2suffix[p]
        )
        done = False
        while not done:
            try:
                mpg_file = root_dir / f"{p}_{time.strftime('%Y%m%d')}.mpg"
                urlretrieve(url, mpg_file)
                done = True
            except Exception:
                time = time - timedelta(days=1)
                url = (
                    root
                    + time.strftime("%Y/%m/%d/")
                    + p2prefix[p]
                    + time.strftime("%Y%m%d")
                    + p2suffix[p]
                )
                continue

        html = mpg_to_html5video(mpg_file)
        soup = BeautifulSoup(html, "html.parser")
        src = soup.find("source")["src"]
        info[p] = src
        time = deepcopy(obstime)

    return info, product_information
