import streamlit as st

from heliodash.packages.sun.hinode.hinode_image import hinode_image

st.markdown(
    """
    # Hinode

    ![Hinode](https://www.nasa.gov/wp-content/uploads/2015/06/541940main_hinode-orig_full.jpg)

    Launch: [Sept. 23, 2006](https://science.nasa.gov/mission/hinode/)
    """
)

st.markdown(
    """
    # Hinode XRT Image

    Source: [NAOJ/Hinode](https://hinode.nao.ac.jp/)
    """
)

info, prod_info = hinode_image()

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
