import streamlit as st

from heliodash.packages.sun.soho.soho_image import soho_image
from heliodash.packages.sun.soho.soho_video import soho_video

st.markdown(
    """
    # SOHO

    ![SOHO](https://assets.science.nasa.gov/dynamicimage/assets/science/psd/solar/2023/07/SOHO_20151202_1600.jpg)

    Launch: [Dec. 2, 1995](https://science.nasa.gov/mission/soho/)
    """
)

plot_type = st.sidebar.selectbox(
    "Plot Type",
    ("Image", "Video"),
)

if plot_type == "Image":
    st.markdown(
        """
        # SOHO EIT and LASCO Images

        Source: [NASA/SOHO](https://soho.nascom.nasa.gov/home.html), [SOHO/EIT](https://umbra.nascom.nasa.gov/eit/)
        """
    )

    products = st.sidebar.multiselect(
        "Products",
        ["171", "195", "284", "304", "c2", "c3"],
        ["171", "195", "284", "304", "c2", "c3"],
    )

    info, prod_info = soho_image(products=products)

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
        # SOHO EIT and LASCO Images

        Source: [NASA/SOHO](https://soho.nascom.nasa.gov/home.html)
        """
    )

    products = st.sidebar.multiselect(
        "Products",
        ["171", "195", "284", "304", "c2", "c3", "c2_combo", "c3_combo"],
        ["171", "195", "284", "304", "c2", "c3", "c2_combo", "c3_combo"],
    )

    info, prod_info = soho_video(products=products)

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
