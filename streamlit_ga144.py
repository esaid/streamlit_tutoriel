import json
import time

import requests
import serial.tools.list_ports
import streamlit as st
from streamlit_ace import st_ace
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


st.set_page_config(layout="wide")
cpu_file = "cpu.json"
lottie_coding = load_lottiefile(cpu_file)

lottie_urlGA144 = "https://assets9.lottiefiles.com/packages/lf20_xafe7wbh.json"
lottie_jsonGA144 = load_lottieurl(lottie_urlGA144)

with st.spinner(text="GA144"):
    st_lottie(lottie_jsonGA144, height=150, key="loading_gif")

original_title = '<p style="font-family:Courier; color:Green; font-size: 40px;">GA144 FORTH</p>'
st.markdown(original_title, unsafe_allow_html=True)

with st.sidebar:
    st_lottie(lottie_coding, speed=0.2, height=150)
    selected_vertical_menu = option_menu("Main Menu", ["Home", 'Settings', 'About'], icons=['house', 'gear'],
                                         menu_icon="cast",
                                         default_index=0)
    node_type = st.selectbox(
        'Node Type Selection :',
        ('NODE', 'GPIO', 'AnalogIn', 'AnalogOut', 'CLK', 'DATA', 'Internal'))
    st.write('NODE Type selected:', node_type)
    list_node=''
    if node_type == 'GPIO':
        list_node = '600', '500', '217', '317', '417', '517', '715'
    if node_type == 'AnalogIn':
        list_node = '117' ,'617', '717' , '713', '709'
    if node_type == 'AnalogOut':
        list_node = '117', '617', '717', '713', '709'
    if node_type == 'CLK':
        list_node = '300' ,'001' ,'701'
    if node_type == 'DATA':
        list_node = '300' , '001', '701'
    node = st.selectbox('Node' , list_node)
    st.write('NODE selected:', node)

selected_horizontal = option_menu(None, ["Home", "Load", 'Save', 'Settings'],
                                  icons=['house', 'bi-file-earmark-arrow-down-fill', 'bi-file-earmark-arrow-up-fill',
                                         'gear'],
                                  menu_icon="cast", default_index=0, orientation="horizontal",
                                  styles={
                                      "container": {"padding": "0!important", "background-color": "#fafafa"},
                                      "icon": {"color": "orange", "font-size": "25px"},
                                      "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                                                   "--hover-color": "#eee"},
                                      "nav-link-selected": {"background-color": "green"},
                                  }
                                  )

code_editeur = st_ace(language='forth', theme='cobalt', font_size=25)
code_editeur

if selected_vertical_menu == 'About':
    st.info('informational message GA144 program ', icon="ℹ️")

if selected_vertical_menu == 'Settings':
    message = ''
    ports = serial.tools.list_ports.comports()
    list_port = []
    for port, desc, hwid in sorted(ports):
        list_port.append(port)
    option_port_serial = st.selectbox('Serial Port selection', list_port)
    st.write('You selected:', option_port_serial)

uploaded_file = st.file_uploader("Choose a file")
