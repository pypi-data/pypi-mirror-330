def soho_video(
    products=[],
):
    product_information = {
        "171": r"EIT 171 Å",
        "195": r"EIT 195 Å",
        "284": r"EIT 284 Å",
        "304": r"EIT 304 Å",
        "c2": r"LASCO C2",
        "c3": r"LASCO C3",
        "c2_combo": r"LASCO C2 Combo",
        "c3_combo": r"LASCO C3 Combo",
    }

    # EIT
    products_eit = ["171", "195", "284", "304"]
    root = "https://soho.nascom.nasa.gov/data/LATEST/current_eit_"
    suffix = ".mp4"
    info = {}
    for p in products:
        if p not in products_eit:
            continue
        image = root + p + suffix
        info[p] = image

    # LASCO
    products_lasco = ["c2", "c3", "c2_combo", "c3_combo"]
    root = "https://soho.nascom.nasa.gov/data/LATEST/current_"
    suffix = ".mp4"
    for p in products:
        if p not in products_lasco:
            continue
        image = root + p + suffix
        info[p] = image

    return info, product_information
