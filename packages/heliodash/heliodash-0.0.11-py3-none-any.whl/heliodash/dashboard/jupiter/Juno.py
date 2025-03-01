from datetime import datetime

import numpy as np
import streamlit as st

from heliodash.packages.jupiter.juno.juno_jiram_image import (
    juno_jiram_ani,
    juno_jiram_image,
    juno_jiram_image_latest,
    juno_jiram_image_list,
    juno_jiram_orbit_list,
    juno_jiram_plot,
)

st.markdown(
    """
    # Juno 

    ![Juno](https://www.nasa.gov/wp-content/uploads/2023/03/pia20704.jpg)
    
    Launch: [Aug. 5, 2011](https://science.nasa.gov/mission/juno/)
    """
)

plot_type = st.sidebar.selectbox(
    "Plot Type",
    ("JIRAM Image"),
)

if plot_type == "JIRAM Image":
    st.markdown(
        """
        # Juno JIRAM Image

        Source: [NASA/PDS](https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/JUNO/jiram.html)
        """
    )

    root = "https://atmos.nmsu.edu/PDS/data/PDS4/juno_jiram_bundle/data_calibrated/"

    cmap = st.sidebar.selectbox(
        "Colormap",
        [
            "hot",
            "gray",
        ],
    )

    latest = st.sidebar.toggle("Latest", value=True)

    # get latest image or select orbit and image
    img_list = None
    if latest:
        with st.spinner("Loading latest image information...", show_time=True):
            img_url = juno_jiram_image_latest()
    else:
        with st.spinner("Loading orbit list...", show_time=True):
            orbit_list = juno_jiram_orbit_list()
            orbit_list = [orbit[:-1] for orbit in orbit_list]
        orbit = st.sidebar.selectbox(
            "Orbit", options=orbit_list, index=len(orbit_list) - 1
        )
        with st.spinner(
            "Loading image list for the selected orbit..", show_time=True
        ):
            img_list = juno_jiram_image_list(orbit + "/")

        img = st.select_slider(
            "Image",
            options=img_list,
            format_func=lambda x: datetime.strptime(
                x[12:-8], "%Y%jT%H%M%S"
            ).strftime("%Y-%m-%d %H:%M:%S"),
            value=img_list[-1],
        )
        img_url = root + orbit + "/" + img

    # display link to label file
    lbl_url = img_url[:-3] + "LBL"
    st.markdown(f"""
    [Label]({lbl_url})         
    """)

    # download and plot image
    with st.spinner("Downloading image...", show_time=True):
        img, info = juno_jiram_image(img_url)
        fig_list = juno_jiram_plot(img, cmap, info)

    for fig in fig_list:
        st.pyplot(fig)

    # create video
    if img_list:
        video = st.sidebar.toggle("Video", value=False)
        if video:
            st.markdown(
                """
                ## Video
                """
            )
            img_list_index = np.arange(len(img_list))
            index_range = st.select_slider(
                "Index Range",
                options=img_list_index,
                value=(0, len(img_list) - 1),
                format_func=lambda x: datetime.strptime(
                    img_list[x][12:-8], "%Y%jT%H%M%S"
                ).strftime("%Y-%m-%d %H:%M:%S"),
            )
            interval = st.number_input(
                "Delay between frames in milliseconds",
                min_value=1,
                max_value=1000,
                value=200,
            )
            stride = st.number_input(
                "Stride", min_value=1, max_value=100, value=1
            )
            img_list_filter = img_list[
                index_range[0] : index_range[1] + 1 : stride
            ]
            if st.button("Create Video"):
                image_url_list = [
                    root + orbit + "/" + image for image in img_list_filter
                ]

                with st.spinner("Creating video...", show_time=True):
                    result = juno_jiram_ani(image_url_list, cmap, interval)
                    for key in result:
                        if result[key]:
                            st.html(result[key])
