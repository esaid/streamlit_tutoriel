import json
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from streamlit_option_menu import option_menu
from streamlit_ace import st_ace


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


cpu_file = "cpu.json"
lottie_coding = load_lottiefile(cpu_file)
original_title = '<p style="font-family:Courier; color:Green; font-size: 40px;">CPU GA144</p>'
st.markdown(original_title, unsafe_allow_html=True)

with st.sidebar:
    st_lottie(lottie_coding, speed=0.5, height=200)
    selected = option_menu("Main Menu", ["Home", 'Settings'], icons=['house', 'gear'], menu_icon="cast",
                           default_index=1)
    selected

selected3 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
                        icons=['house', 'cloud-upload', "list-task", 'gear'],
                        menu_icon="cast", default_index=0, orientation="horizontal",
                        styles={
                            "container": {"padding": "0!important", "background-color": "#fafafa"},
                            "icon": {"color": "orange", "font-size": "25px"},
                            "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                                         "--hover-color": "#eee"},
                            "nav-link-selected": {"background-color": "green"},
                        }
                        )

content = st_ace(language='forth', theme='cobalt', font_size=25)
content
