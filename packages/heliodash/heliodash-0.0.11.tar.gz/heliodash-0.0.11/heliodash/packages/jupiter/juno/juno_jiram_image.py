# https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/JUNO/jiram.html
# https://atmos.nmsu.edu/PDS/data/PDS4/juno_jiram_bundle/document/JIRAM_SIS_V7.5.pdf
# UNIT (Page 29-31)
# RDR-IMG DATA (Image) - band radiance  [W/(m^2 sterad)]
# MODE (Page 54)
# I0 - no IMAGE
# I1 - IMAGE(256x432) L and M band
# I2 - IMAGE(128x432) M-band
# I3 - IMAGE(128x432) L-band

import re
from datetime import datetime
from pathlib import Path
from urllib.request import urlretrieve

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from heliodash.packages.jupiter.juno.pds_parser import read_label
from heliodash.packages.util.html_parser import get_bs

dataroot = Path("./data")
dataroot.mkdir(exist_ok=True)


@st.cache_data(show_spinner=False)
def juno_jiram_orbit_list():
    root = "https://atmos.nmsu.edu/PDS/data/PDS4/juno_jiram_bundle/data_calibrated/"
    bs = get_bs(root)
    orbit_list = bs.find_all("a", {"href": re.compile(r"^orbit(\d+)/")})
    orbit_list = [orbit["href"] for orbit in orbit_list]
    return sorted(orbit_list)


@st.cache_data(show_spinner=False)
def juno_jiram_image_list(orbit):
    root = (
        "https://atmos.nmsu.edu/PDS/data/PDS4/juno_jiram_bundle/data_calibrated/"
        + orbit
    )
    bs = get_bs(root)
    img_list = bs.find_all("a", {"href": re.compile(r"^.*\.IMG$")})
    img_list = [img["href"] for img in img_list]
    return sorted(img_list)


def juno_jiram_image_latest():
    orbit_list = juno_jiram_orbit_list()
    orbit = orbit_list[-1]
    img_list = juno_jiram_image_list(orbit)
    img = img_list[-1]
    img_url = (
        "https://atmos.nmsu.edu/PDS/data/PDS4/juno_jiram_bundle/data_calibrated/"
        + orbit
        + img
    )
    return img_url


@st.cache_data(show_spinner=False)
def juno_jiram_image(img_url):
    img_name = img_url[-34:]
    urlretrieve(img_url, dataroot / img_name)

    lbl_url = img_url[:-3] + "LBL"
    lbl_name = img_name[:-3] + "LBL"
    urlretrieve(lbl_url, dataroot / lbl_name)

    lbl = read_label(dataroot / lbl_name)
    modestr = str(lbl["INSTRUMENT_MODE_ID"])
    if "I1" in modestr:
        nx = 256
        ny = 432
        band = "L and M"
    elif "I2" in modestr:
        nx = 128
        ny = 432
        band = "M"
    elif "I3" in modestr:
        nx = 128
        ny = 432
        band = "L"

    img = np.fromfile(dataroot / img_name, dtype="<f4")
    img = img.reshape((nx, ny))
    time_str = datetime.strptime(img_name[12:-8], "%Y%jT%H%M%S").strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    # time_str = datetime.strptime(str(lbl["START_TIME"])[:-4], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    time_str = time_str + " UTC"

    info = {}
    info["time_str"] = time_str
    info["band"] = band
    return img, info


def juno_jiram_plot(img, cmap, info):
    time_str = info["time_str"]
    # fig, ax = plt.subplots(figsize=(8, 4))
    # cax = ax.imshow(img, cmap=cmap, vmin=0, origin='lower')
    # divider = make_axes_locatable(ax)
    # cax_colorbar = divider.append_axes("right", size="2.5%", pad=0.1)
    # fig.colorbar(cax, cax=cax_colorbar, label='band radiance [W m$^{-2}$ sr$^{-1}$]', location='right')
    # ax.set_title(time_str)
    # fig.tight_layout()
    # return fig
    if img.shape[0] == 128:
        img_list = [img]
    else:
        img_list = [img[:128, :], img[128:, :]]

    fig_list = []
    for img in img_list:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.imshow(img, cmap=cmap, vmin=0, origin="lower")
        ax.axis("off")
        ax.set_title(time_str)
        fig.tight_layout()
        fig_list.append(fig)
        plt.close(fig)

    return fig_list


def juno_jiram_ani(img_url_list, cmap, interval=200):
    img_256_list_1st = []
    img_256_list_2nd = []
    img_128_M_list = []
    img_128_L_list = []

    progress_text = "Downloading data..."
    total = len(img_url_list)
    my_bar = st.progress(0, text=progress_text)
    for i, img_url in enumerate(img_url_list):
        img, info = juno_jiram_image(img_url)

        if info["band"] == "L and M":
            img_256_list_1st.append(
                {"img": img[:128, :], "info": info, "cmap": cmap}
            )
            img_256_list_2nd.append(
                {"img": img[128:, :], "info": info, "cmap": cmap}
            )
        elif info["band"] == "M":
            img_128_M_list.append({"img": img, "info": info, "cmap": cmap})
        elif info["band"] == "L":
            img_128_L_list.append({"img": img, "info": info, "cmap": cmap})

        percent_complete = int((i + 1) / total * 100)
        my_bar.progress(percent_complete, text=f"{progress_text} {i}/{total}")
    my_bar.empty()

    if len(img_256_list_1st) > 0:
        ani_256_1st = get_ani(img_256_list_1st, interval)
    else:
        ani_256_1st = None

    if len(img_256_list_2nd) > 0:
        ani_256_2nd = get_ani(img_256_list_2nd, interval)
    else:
        ani_256_2nd = None

    if len(img_128_M_list) > 0:
        ani_128_M = get_ani(img_128_M_list, interval)
    else:
        ani_128_M = None

    if len(img_128_L_list) > 0:
        ani_128_L = get_ani(img_128_L_list, interval)
    else:
        ani_128_L = None

    result = {
        "256_1st": ani_256_1st,
        "256_2nd": ani_256_2nd,
        "128_M": ani_128_M,
        "128_L": ani_128_L,
    }
    return result


def get_ani(img_list, interval=200):
    fig, ax = plt.subplots(figsize=(8, 4))

    def update(frame):
        data = img_list[frame]
        img = data["img"]
        time = data["info"]["time_str"]
        cmap = data["cmap"]

        ax.clear()
        ax.imshow(img, cmap=cmap, vmin=0, origin="lower")
        ax.axis("off")
        ax.set_title(time)

    ani = animation.FuncAnimation(
        fig, update, frames=len(img_list), interval=interval
    )
    return ani.to_html5_video()
