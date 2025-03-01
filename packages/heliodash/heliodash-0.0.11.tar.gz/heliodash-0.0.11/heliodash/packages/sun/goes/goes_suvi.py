"""
https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes
"""


def goes_suvi_image(
    primary=True, products=["094", "131", "171", "195", "284", "304", "map"]
):
    product_information = {
        "094": r"SUVI 094 Å",
        "131": r"SUVI 131 Å",
        "171": r"SUVI 171 Å",
        "195": r"SUVI 195 Å",
        "284": r"SUVI 284 Å",
        "304": r"SUVI 304 Å",
        "map": r"SUVI Thematic Map",
    }

    sat_class = "primary" if primary else "secondary"

    root = (
        f"https://services.swpc.noaa.gov/images/animations/suvi/{sat_class}/"
    )
    suffix = "/latest.png"

    info = {}
    for p in products:
        image = root + p + suffix
        info[p] = image

    return info, product_information
