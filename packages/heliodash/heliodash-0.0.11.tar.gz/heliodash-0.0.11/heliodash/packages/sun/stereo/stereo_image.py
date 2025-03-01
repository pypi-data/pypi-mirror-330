import re
from copy import deepcopy
from datetime import datetime, timedelta, timezone

from heliodash.packages.util.html_parser import get_bs


def stereo_image(
    products=[],
    latest_available=False,
):
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

    # very latest images
    if not latest_available:
        product2file = {
            "A_171": "ahead_euvi_171",
            "A_195": "ahead_euvi_195",
            "A_284": "ahead_euvi_284",
            "A_304": "ahead_euvi_304",
            "A_COR1": "ahead_cor1",
            "A_COR2": "ahead_cor2",
            "B_171": "behind_euvi_171",
            "B_195": "behind_euvi_195",
            "B_284": "behind_euvi_284",
            "B_304": "behind_euvi_304",
            "B_COR1": "behind_cor1",
            "B_COR2": "behind_cor2",
        }

        root = "https://stereo-ssc.nascom.nasa.gov/beacon/latest/"
        suffix = "_latest.jpg"
        info = {}
        for p in products:
            if p not in product_information:
                continue
            image = root + product2file[p] + suffix
            info[p] = image

    # latest available images
    if latest_available:
        obstime = datetime.now(timezone.utc)

        root = "https://stereo-ssc.nascom.nasa.gov/browse/"
        pattern = re.compile(
            r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2}).*.jpg"
        )

        p2source = {
            "A_171": "ahead/euvi/171/2048/",
            "A_195": "ahead/euvi/195/2048/",
            "A_284": "ahead/euvi/284/2048/",
            "A_304": "ahead/euvi/304/2048/",
            "A_COR1": "ahead/cor1/1024/",
            "A_COR2": "ahead/cor2/1024/",
            "B_171": "behind/euvi/171/2048/",
            "B_195": "behind/euvi/195/2048/",
            "B_284": "behind/euvi/284/2048/",
            "B_304": "behind/euvi/304/2048/",
            "B_COR1": "behind/cor1/1024/",
            "B_COR2": "behind/cor2/1024/",
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
            url = root + time.strftime("%Y/%m/%d/") + p2source[p]
            bs = get_bs(url)
            # if the page doesn't exist, try the previous day until we find a page that exists
            while bs is None:
                time = time - timedelta(days=1)
                url = root + time.strftime("%Y/%m/%d/") + p2source[p]
                bs = get_bs(url)
            img_list = bs.find_all("a", {"href": pattern})
            href_list = [img["href"] for img in img_list]
            href_list = sorted(href_list)
            latest = href_list[-1]
            img_url = url + latest
            info[p] = img_url
            time = deepcopy(obstime)

    return info, product_information
