import streamlit as st

from heliodash.packages.sun.sdo.sdo_image import sdo_image
from heliodash.packages.sun.sdo.sdo_video import sdo_video

st.markdown(
    """
    # SDO

    ![SDO](https://www.nasa.gov/wp-content/uploads/2023/03/421359main_226837main_SDOconcept2_HI_full.jpg)

    Launch: [Feb. 11, 2010](https://science.nasa.gov/mission/sdo/)
    """
)

plot_type = st.sidebar.selectbox(
    "Plot Type",
    ("Image", "Video"),
)

if plot_type == "Image":
    st.markdown(
        """
        # SDO AIA and HMI Images

        Source: [NASA/SDO](https://sdo.gsfc.nasa.gov/)
        """
    )
    list_of_products = (
        "0094",
        "0131",
        "0171",
        "0193",
        "0211",
        "0304",
        "0335",
        "1600",
        "1700",
        "304_211_171",
        "094_335_193",
        "HMImag_171",
        "HMIB",
        "HMIBC",
        "HMII",
        "HMIIC",
        "HMIIF",
        "HMID",
    )

    products = st.sidebar.multiselect(
        "Products",
        list_of_products,
        list_of_products,
    )
    pfss = st.sidebar.toggle("PFSS", value=False)

    info, prod_info = sdo_image(products=products, pfss=pfss)

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
        # SDO AIA Videos

        Source: [NASA/SDO](https://sdo.gsfc.nasa.gov/)
        """
    )
    list_of_products = (
        "0094",
        "0131",
        "0171",
        "0193",
        "0211",
        "0304",
        "0335",
        "1600",
        "1700",
    )

    products = st.sidebar.multiselect(
        "Products",
        list_of_products,
        list_of_products,
    )

    info, prod_info = sdo_video(products=products)

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
            <h2>{prod_info[p]}<br>48 hours</h2>
            <video width="100%" autoplay loop muted playsinline controls>
                <source src="{info[p]}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        """
        st.html(html_code)
