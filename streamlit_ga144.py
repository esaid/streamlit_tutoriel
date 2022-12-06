import json

import requests
import serial.tools.list_ports
import streamlit as st
from streamlit_ace import st_ace
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu


def load_lottieurl(url: str):
    r = requests.get ( url )
    if r.status_code != 200:
        return None
    return r.json ()


def load_lottiefile(filepath: str):
    with open ( filepath, "r" ) as f:
        return json.load ( f )


cpu_file = "cpu.json"
lottie_coding = load_lottiefile ( cpu_file )

lottie_urlGA144 = "https://assets9.lottiefiles.com/packages/lf20_xafe7wbh.json"
lottie_jsonGA144 = load_lottieurl ( lottie_urlGA144 )

with st.spinner ( text="GA144" ):
    st_lottie ( lottie_jsonGA144, height=100, key="loading_gif" )

original_title = '<p style="font-family:Courier; color:Green; font-size: 40px;">GA144 FORTH</p>'
st.markdown ( original_title, unsafe_allow_html=True )

with st.sidebar:
    st_lottie ( lottie_coding, speed=0.2, height=150 )
    selected = option_menu ( "Main Menu", ["Home", 'Settings', 'About'], icons=['house', 'gear'], menu_icon="cast",
                             default_index = 1 )

selected3 = option_menu ( None, ["Home", "Upload", 'Settings'],
                          icons=['house', 'cloud-upload', 'gear'],
                          menu_icon="cast", default_index=0, orientation="horizontal",
                          styles={
                              "container": {"padding": "0!important", "background-color": "#fafafa"},
                              "icon": {"color": "orange", "font-size": "25px"},
                              "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                                           "--hover-color": "#eee"},
                              "nav-link-selected": {"background-color": "green"},
                          }
                          )

content = st_ace ( language='forth', theme='cobalt', font_size=25 )
content
if selected == 'About':
    st.info ( 'informational message GA144 program ', icon="ℹ️" )

if selected == 'Settings':
    message = ''
    ports = serial.tools.list_ports.comports ()
    type ( ports )
    for port, desc, hwid in sorted ( ports ):
        message +=  "  \n" + port
    st.info ( f"list port : {message} " )
