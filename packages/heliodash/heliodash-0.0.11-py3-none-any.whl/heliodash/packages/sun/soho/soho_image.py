import re

from heliodash.packages.util.html_parser import get_bs


def soho_image(
    products=[],
):
    product_information = {
        "171": r"EIT 171 Å",
        "195": r"EIT 195 Å",
        "284": r"EIT 284 Å",
        "304": r"EIT 304 Å",
        "c2": r"LASCO C2",
        "c3": r"LASCO C3",
    }

    # EIT
    bs = get_bs("https://umbra.nascom.nasa.gov/eit/eit_full_res.html")
    for td in bs.find_all("td"):
        text = td.get_text(strip=True)
        date = re.findall(r"\d{4}/\d{2}/\d{2}.*\d{2}:\d{2}:\d{2}", text)[0]
        if len(date) > 0:
            break
    obstimes = tuple([date[i : i + 19] for i in range(0, len(date), 19)])
    product_information["171"] += "<br>" + obstimes[0]
    product_information["195"] += "<br>" + obstimes[1]
    product_information["284"] += "<br>" + obstimes[2]
    product_information["304"] += "<br>" + obstimes[3]

    products_eit = ["171", "195", "284", "304"]
    root = "https://umbra.nascom.nasa.gov/eit/images/latest_eit_"
    suffix = "_full.gif"
    info = {}
    for p in products:
        if p not in products_eit:
            continue
        image = root + p + suffix
        info[p] = image

    # LASCO
    products_lasco = ["c2", "c3"]
    root = "https://soho.nascom.nasa.gov/data/realtime/"
    suffix = "/1024/latest.jpg"
    for p in products:
        if p not in products_lasco:
            continue
        image = root + p + suffix
        info[p] = image

    return info, product_information
