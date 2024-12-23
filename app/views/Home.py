import streamlit as st
import os, sys, json
# import uuid
from datetime import datetime


# Embed the Styles
css_styles = ""
css_files = ["login.css"]
for css_file in css_files:
    with open(os.path.join(st.session_state["styles_dr"], css_file)) as f:
        css = f.read()
    css_styles += f"{css}\n"
# st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
st.html(f"<style>{css_styles}</style>")

st.markdown(
    "<h1 style='text-align: center; color: #0D6EFD;'>Home</h1>",
    unsafe_allow_html=True
)