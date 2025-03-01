import streamlit as st

from heliodash.packages.sun.stereo.stereo_image import stereo_image
from heliodash.packages.sun.stereo.stereo_video import stereo_video

st.markdown(
    """
    # STEREO

    ![STEREO](https://www.jhuapl.edu/sites/default/files/2024-03/IMG-Mission-STEREO.jpg)

    Launch: [Oct. 26, 2006](https://science.nasa.gov/mission/stereo/)
    """
)


plot_type = st.sidebar.selectbox(
    "Plot Type",
    ("Image", "Video"),
)


if plot_type == "Image":
    latest_available = st.sidebar.toggle(
        "Show Latest Available Image", value=False
    )

    st.markdown(
        """
        # STEREO EUVI and COR Images

        Source: [NASA/SSC](https://stereo-ssc.nascom.nasa.gov/)
        """
    )

    list_of_products = (
        "A_171",
        "A_195",
        "A_284",
        "A_304",
        "A_COR1",
        "A_COR2",
        "B_171",
        "B_195",
        "B_284",
        "B_304",
        "B_COR1",
        "B_COR2",
    )

    products = st.sidebar.multiselect(
        "Products",
        list_of_products,
        list_of_products,
    )

    with st.spinner("Loading images...", show_time=True):
        info, prod_info = stereo_image(
            products=products, latest_available=latest_available
        )

    for p in products:
        html_code = f"""
        <div style="
            border: 2px solid #000000; 
            padding: 10px; 
            display: inline-block;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            text-align: center;
        ">  
            <h2>{prod_info[p]}</h2>
            <img src="{info[p]}" width="100%">
        </div>
        """

        st.html(html_code)

if plot_type == "Video":
    st.markdown(
        """
        # STEREO EUVI and COR Videos

        Source: [NASA/SSC](https://stereo-ssc.nascom.nasa.gov/)
        """
    )

    list_of_products = (
        "A_171",
        "A_195",
        "A_284",
        "A_304",
        "A_COR1",
        "A_COR2",
        "B_171",
        "B_195",
        "B_284",
        "B_304",
        "B_COR1",
        "B_COR2",
    )

    products = st.sidebar.multiselect(
        "Products",
        list_of_products,
        list_of_products,
    )

    with st.spinner("Loading videos...", show_time=True):
        info, prod_info = stereo_video(products=products)

    for p in products:
        html_code = f"""
        <div style="
            border: 2px solid #000000; 
            padding: 10px; 
            display: inline-block;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            text-align: center;
        ">  
            <h2>{prod_info[p]}</h2>
            <video width="100%" autoplay loop muted playsinline controls>
                <source src="{info[p]}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        """
        st.html(html_code)
