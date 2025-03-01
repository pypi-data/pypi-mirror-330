def sdo_video(
    products=[],
):
    product_information = {
        "0094": r"AIA 094 Å",
        "0131": r"AIA 131 Å",
        "0171": r"AIA 171 Å",
        "0193": r"AIA 193 Å",
        "0211": r"AIA 211 Å",
        "0304": r"AIA 304 Å",
        "0335": r"AIA 335 Å",
        "1600": r"AIA 1600 Å",
        "1700": r"AIA 1700 Å",
    }

    root = "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_"
    suffix = ".mp4"
    info = {}
    for p in products:
        video = root + p + suffix
        info[p] = video

    return info, product_information
