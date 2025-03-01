import streamlit as st

from heliodash.packages.sun.proba2.proba2_image import proba2_image

st.markdown(
    """
    # PROBA-2

    ![PROBA22](https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2009/05/proba-2_artist_impression/9701242-3-eng-GB/Proba-2_artist_impression_pillars.jpg)

    Launch: [Nov. 2, 2009](https://proba2.sidc.be/about/mission)
    """
)

st.info("Under development...")

st.markdown(
    """
    # PROBA-2 SWAP Image

    Source: [ESA/PROBA2/SWAP](https://proba2.sidc.be/data/SWAP)
    """
)

info, prod_info = proba2_image()

html_code = f"""
<div style="
    border: 2px solid #000000; 
    padding: 10px; 
    display: inline-block;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    text-align: center;
">  
    <h2>{prod_info}</h2>
    <img src="{info}" width="100%">
</div>
"""

st.html(html_code)
