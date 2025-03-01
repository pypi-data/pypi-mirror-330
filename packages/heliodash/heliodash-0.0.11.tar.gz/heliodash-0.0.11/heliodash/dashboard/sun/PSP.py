from datetime import datetime
from pathlib import Path

import streamlit as st

from heliodash.packages.sun.psp.psp_image import (
    psp_wispr_combined_plot,
    psp_wispr_date_list,
    psp_wispr_fits_list,
    psp_wispr_image,
    psp_wispr_image_latest,
    psp_wispr_orbit_list,
    psp_wispr_plot,
)


def plot(repro, img_url):
    with st.spinner("Downloading image...", show_time=True):
        img = psp_wispr_image(img_url)

    fig_list = []

    if repro == "Both":
        fig_list.append(psp_wispr_plot(img))
        fig_list.append(psp_wispr_plot(img, reproject=True))
    elif repro == "Original":
        fig_list.append(psp_wispr_plot(img))
    else:
        fig_list.append(psp_wispr_plot(img, reproject=True))

    for fig in fig_list:
        st.pyplot(fig)


# def make_video(img_list):
#     img_list_index = np.arange(len(img_list))
#     index_range = st.select_slider(
#         "Index Range",
#         options=img_list_index,
#         value=(0, len(img_list) - 1),
#         format_func=lambda x: dt(img_list[x]),
#     )
#     interval = st.number_input(
#         "Delay between frames in milliseconds",
#         min_value=1,
#         max_value=1000,
#         value=200,
#     )
#     stride = st.number_input(
#         "Stride", min_value=1, max_value=100, value=1
#     )
#     img_list_filter = img_list[
#         index_range[0] : index_range[1] + 1 : stride
#     ]

#     if st.button("Create Video"):
#         image_url_list = [
#             root + orbit + "/" + date + "/" + image for image in img_list_filter
#         ]

#         with st.spinner("Creating video...", show_time=True):
#             ani = psp_wispr_ani(image_url_list, interval)
#             st.html(ani)

st.markdown(
    """
    # Parker Solar Probe

    ![PSP](https://parkersolarprobe.jhuapl.edu/Multimedia/ApprovedMedia/Images/Renderings/md/PSP-inFrontOfSun.jpg)

    Launch: [Aug. 12, 2018](https://science.nasa.gov/mission/parker-solar-probe/)
    """
)

plot_type = st.sidebar.selectbox(
    "Plot Type",
    ("PSP Image"),
)

if plot_type == "PSP Image":
    st.markdown(
        """
        ## PSP WISPR Image

        ![](https://wispr.nrl.navy.mil/sites/wispr.nrl.navy.mil/files/images/WISPR%20FOV-01.jpg)

        Source: [NRL/WISPR](https://wispr.nrl.navy.mil/)
        """
    )

    root = "https://wispr.nrl.navy.mil/data/rel/fits/L3/"

    repro = st.sidebar.selectbox(
        "Show Image", ("Both", "Original", "Reprojected"), index=2
    )

    latest = st.sidebar.toggle("Latest", value=True)

    # get latest image or select orbit and image
    img_list = None
    if latest:
        with st.spinner("Loading latest image information...", show_time=True):
            img_url = psp_wispr_image_latest()
        plot(repro, img_url)
    else:
        with st.spinner("Loading orbit list...", show_time=True):
            orbit_list = psp_wispr_orbit_list()
            orbit_list = [orbit[:-1] for orbit in orbit_list]
        orbit = st.sidebar.selectbox(
            "Orbit", options=orbit_list, index=len(orbit_list) - 1
        )
        with st.spinner(
            "Loading date list for the selected orbit..", show_time=True
        ):
            date_list = psp_wispr_date_list(orbit + "/")
            date_list = [date[:-1] for date in date_list]

        date = st.sidebar.selectbox(
            "Date", options=date_list, index=len(date_list) - 1
        )

        with st.spinner(
            "Loading fits list for the selected date...", show_time=True
        ):
            fits_list = psp_wispr_fits_list(orbit + "/", date + "/")

        def dt(x):
            return datetime.strptime(x[13:-13], "%Y%m%dT%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        split = st.sidebar.checkbox("Inner/Outer", value=False)
        if split:
            inner_fits_list = [
                f for f in fits_list if f.split(".")[0][-4:] == "1221"
            ]
            outer_fits_list = [
                f for f in fits_list if f.split(".")[0][-4:] == "2222"
            ]

            if len(inner_fits_list) > 0:
                st.info(f"{len(inner_fits_list)} inner fits found.")
                inner_fits = st.select_slider(
                    "Inner FITS",
                    options=inner_fits_list,
                    format_func=dt,
                    value=inner_fits_list[-1],
                )
                img_url = root + orbit + "/" + date + "/" + inner_fits
                plot(repro, img_url)
                # video = st.sidebar.toggle("Video (Inner)", value=False)
                # if video:
                #     st.markdown(
                #         """
                #         ### Video (Inner)
                #         """
                #     )
                #     make_video(inner_fits_list)
            else:
                inner_fits = None
                st.warning("No inner fits found.")

            if len(outer_fits_list) > 0:
                st.info(f"{len(outer_fits_list)} outer fits found.")
                outer_fits = st.select_slider(
                    "Outer FITS",
                    options=outer_fits_list,
                    format_func=dt,
                    value=outer_fits_list[-1],
                )
                img_url = root + orbit + "/" + date + "/" + outer_fits
                plot(repro, img_url)
                # video = st.sidebar.toggle("Video (Outer)", value=False)
                # if video:
                #     st.markdown(
                #         """
                #         ### Video (Outer)
                #         """
                #     )
                #     make_video(outer_fits_list)
            else:
                outer_fits = None
                st.warning("No outer fits found.")

            if inner_fits and outer_fits:
                combined = st.sidebar.checkbox("Combined", value=False)
                if combined:
                    dataroot = Path("./data")

                    inner_idx = st.sidebar.number_input("Inner Index", value=0)
                    outer_idx = st.sidebar.number_input("Outer Index", value=0)
                    st.markdown(
                        """
                        ## Combined Plot
                        """
                    )
                    fig = psp_wispr_combined_plot(
                        dataroot / inner_fits_list[inner_idx],
                        dataroot / outer_fits_list[outer_idx],
                    )
                    st.pyplot(fig)

        else:
            fits = st.select_slider(
                "FITS",
                options=fits_list,
                format_func=lambda x: x[13:],
                value=fits_list[-1],
            )

            img_url = root + orbit + "/" + date + "/" + fits
            plot(repro, img_url)
