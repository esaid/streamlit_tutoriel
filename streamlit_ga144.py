import json
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from streamlit_option_menu import option_menu


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


cpu_file = "cpu.json"
lottie_coding = load_lottiefile(cpu_file)
original_title = '<p style="font-family:Courier; color:Green; font-size: 40px;">CPU GA144</p>'
st.markdown(original_title, unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<p style="font-family:Courier;  font-size: 25px;">MENU</p>', unsafe_allow_html=True)
    st_lottie.st_lottie(lottie_coding, speed=0.5, height=200)
