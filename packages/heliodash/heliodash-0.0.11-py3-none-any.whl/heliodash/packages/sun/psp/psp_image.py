import re
import ssl
from pathlib import Path
from urllib.request import urlopen

import astropy.units as u
import astropy.wcs
import matplotlib.pyplot as plt
import streamlit as st
from astropy.coordinates import SkyCoord
from astropy.visualization import ImageNormalize, PowerStretch
from reproject import reproject_interp
from reproject.mosaicking import reproject_and_coadd
from sunpy.coordinates import Helioprojective
from sunpy.coordinates.screens import SphericalScreen
from sunpy.map import Map, make_fitswcs_header

from heliodash.packages.util.html_parser import get_bs

wispr_norm = ImageNormalize(
    vmin=0, vmax=0.5e-11, stretch=PowerStretch(1 / 2.2)
)


dataroot = Path("./data")
dataroot.mkdir(exist_ok=True)


@st.cache_data(show_spinner=False)
def psp_wispr_orbit_list():
    root = "https://wispr.nrl.navy.mil/data/rel/fits/L3/"
    bs = get_bs(root, allow_unverified=True)
    orbit_list = bs.find_all("a", {"href": re.compile(r"^orbit(\d+)/")})
    orbit_list = [orbit["href"] for orbit in orbit_list]
    return sorted(orbit_list)


@st.cache_data(show_spinner=False)
def psp_wispr_date_list(orbit):
    root_orbit = "https://wispr.nrl.navy.mil/data/rel/fits/L3/" + orbit
    bs_orbit = get_bs(root_orbit, allow_unverified=True)
    date_list = bs_orbit.find_all("a", {"href": re.compile(r"^\d{8}/")})
    date_list = [date["href"] for date in date_list]
    return sorted(date_list)


@st.cache_data(show_spinner=False)
def psp_wispr_fits_list(orbit, date):
    root_orbit_date = (
        "https://wispr.nrl.navy.mil/data/rel/fits/L3/" + orbit + date
    )
    bs_orbit_date = get_bs(root_orbit_date, allow_unverified=True)
    fits_list = bs_orbit_date.find_all("a", {"href": re.compile(r"\.fits$")})
    fits_list = [fits["href"] for fits in fits_list]
    return sorted(fits_list)


def psp_wispr_image_latest():
    orbit_list = psp_wispr_orbit_list()
    orbit = orbit_list[-1]
    date_list = psp_wispr_date_list(orbit)
    date = date_list[-1]
    fits_list = psp_wispr_fits_list(orbit, date)
    fits_name = fits_list[-1]
    fits_url = (
        "https://wispr.nrl.navy.mil/data/rel/fits/L3/"
        + orbit
        + date
        + fits_name
    )
    return fits_url


@st.cache_data(show_spinner=False)
def psp_wispr_image(fits_url):
    fits_name = fits_url.split("/")[-1]
    fits_path = dataroot / fits_name
    with (
        urlopen(
            fits_url, context=ssl._create_unverified_context()
        ) as response,
        open(fits_path, "wb") as out_file,
    ):
        out_file.write(response.read())

    return fits_path


def psp_wispr_plot(fits_file, reproject=False):
    smap = Map(fits_file)
    fig = plt.figure(figsize=(10, 10))

    if reproject:
        m_smap = wispr_maps(smap)
        m_smap.plot(norm=wispr_norm)
        m_smap.draw_limb(color="w")
    else:
        smap.plot(norm=wispr_norm)
    return fig


def psp_wispr_combined_plot(inner_fits_file, outer_fits_file):
    inner_smap = Map(inner_fits_file)
    outer_smap = Map(outer_fits_file)

    fig = plt.figure(figsize=(10, 10))
    m_smap = combine_wispr_maps(inner_smap, outer_smap)
    m_smap.plot(norm=wispr_norm)
    m_smap.draw_limb(color="w")
    return fig


# https://github.com/heliophysicsPy/summer-school-24/blob/main/sunpy-tutorial/sunpy-pyspedas-showcase/sunpy-pyspedas-demo.ipynb


def wispr_maps(smap):
    ref_coord = SkyCoord(
        0 * u.arcsec,
        0 * u.arcsec,
        frame=Helioprojective(
            observer=smap.observer_coordinate, obstime=smap.date
        ),
    )

    outshape = (360 * 2, int(360 * 3.5))
    new_header = make_fitswcs_header(
        outshape,
        ref_coord,
        reference_pixel=u.Quantity([40 * u.pixel, 500 * u.pixel]),
        scale=u.Quantity([0.1 * u.deg / u.pixel, 0.1 * u.deg / u.pixel]),
        projection_code="CAR",
    )
    out_wcs = astropy.wcs.WCS(new_header)
    with SphericalScreen(smap.observer_coordinate):
        array, footprint = reproject_and_coadd(
            [smap],
            out_wcs,
            outshape,
            reproject_function=reproject_interp,
            match_background=True,
        )

    combined_map = Map((array, new_header))
    return combined_map


def combine_wispr_maps(inner_map, outer_map):
    ref_coord = SkyCoord(
        0 * u.arcsec,
        0 * u.arcsec,
        frame=Helioprojective(
            observer=inner_map.observer_coordinate, obstime=inner_map.date
        ),
    )

    outshape = (360 * 2, int(360 * 3.5))
    new_header = make_fitswcs_header(
        outshape,
        ref_coord,
        reference_pixel=u.Quantity([40 * u.pixel, 500 * u.pixel]),
        scale=u.Quantity([0.1 * u.deg / u.pixel, 0.1 * u.deg / u.pixel]),
        projection_code="CAR",
    )
    out_wcs = astropy.wcs.WCS(new_header)
    with SphericalScreen(inner_map.observer_coordinate):
        array, footprint = reproject_and_coadd(
            (inner_map, outer_map),
            out_wcs,
            outshape,
            reproject_function=reproject_interp,
            match_background=True,
        )

    combined_map = Map((array, new_header))
    return combined_map


# def psp_wispr_ani(img_url_list, interval=200, reproject=False):
#     progress_text = "Downloading data..."
#     total = len(img_url_list)
#     my_bar = st.progress(0, text=progress_text)
#     img_list = []
#     for i, img_url in enumerate(img_url_list):
#         img_list.append(psp_wispr_image(img_url))

#         percent_complete = int((i + 1) / total * 100)
#         my_bar.progress(percent_complete, text=f"{progress_text} {i}/{total}")
#     my_bar.empty()

#     print(img_list)

#     ani = get_ani(img_list, interval, reproject)
#     return ani

# def get_ani(img_list, interval=200, reproject=False):
#     map_list = [Map(img) for img in img_list]
#     fig = plt.figure(figsize=(10, 10))

#     if reproject:
#         map_list = [wispr_maps(smap) for smap in map_list]

#     ax = fig.add_subplot(projection=map_list[0].wcs)
#     def update(frame, ax):
#         ax.clear()
#         map_list[frame].plot(norm=wispr_norm, axes=ax)
#     ani = animation.FuncAnimation(
#         fig, update, frames=len(map_list), interval=interval, fargs=(ax,)
#     )

#     return ani.to_html5_video()
