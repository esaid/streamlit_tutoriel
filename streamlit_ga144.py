import json
import os
import time
from io import StringIO

import requests
import serial.tools.list_ports
import streamlit as st
from streamlit_ace import st_ace
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from itertools import cycle


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

original_title = '<p style="font-family:Courier; color:Green; font-size: 40px;">GA144 FORTH</p>'
st.markdown(original_title, unsafe_allow_html=True)

with st.spinner(text="GA144"):
    st_lottie(lottie_jsonGA144, height=150, key="loading_gif")

with st.sidebar:
    st_lottie(lottie_coding, speed=0.2, height=150)
    selected_vertical_menu = option_menu("Main Menu", ["Home", 'Settings', 'About'], icons=['house', 'gear'],
                                         menu_icon="cast",
                                         default_index=0)
    node_type = st.selectbox(
        'Node Type Selection :',
        ('NODE', 'GPIO', 'Analog-In', 'Analog-Out', 'CLK', 'DATA', 'Internal'))

    list_node = ''
    if node_type == 'GPIO':
        list_node = '600', '500', '217', '317', '417', '517', '715'
    if node_type == 'Analog-In':
        list_node = '117', '617', '717', '713', '709'
    if node_type == 'Analog-Out':
        list_node = '117', '617', '717', '713', '709'
    if node_type == 'CLK':
        list_node = '300', '001', '701'
    if node_type == 'DATA':
        list_node = '300', '001', '701'
    if node_type == 'Internal':
        list_node = '002', '003', '004', '005', '006', '010', '011', '012', '013', '014', '015', '016', '017', '101', '102', '103', '104', '105', '106', '107', \
                    '108', '109', '110', '111', '112', '113', '114', '115', '116', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', \
                    '213', '214', '215', '216', '300', '301', '302', '303', '304', '305', '306', '307', '308', '309', '310', '311', '312', '313', '314', '315', '316', \
                    '400', '401', '402', '403', '404', '405', '406', '407', '408', '409', '410', '411', '412', '413', '414', '415', '416', \
                    '501', '502', '503', '504', '505', '506', '507', '508', '509', '510', '511', '512', '513', '514', '515', '516', \
                    '601', '602', '603', '604', '605', '606', '607', '608', '609', '610', '611', '612', '613', '614', '615', '616', \
                    '700', '701', '702', '703', '704', '706', '707', '708', '710', '711', '712', '714', '716'

    node = st.selectbox('Node', list_node)
    st.write('NODE Type selected:', node_type)
    st.write('NODE selected:', node)

with st.container():
    cwd = os.getcwd()  # folder
    projet = st.text_input('Project :  👇')
    st.write(f"Current working directory: {cwd}")

    if not projet:
        st.warning('Please input a name directory project')
        st.stop()

    st.success('Thank you for inputting a name.')
    path = os.path.join(cwd, projet)
    try:
        os.mkdir(path)
    except OSError as errordirectory:
        st.error(f'This is an error  {errordirectory}', icon="🚨")
        st.stop()
    os.chdir(path)  # path_initial /projet
    st.info(f'Create init.ga file in {projet}', icon="ℹ️")
    init_text = '( init file )\n'
    with open('init.ga', "w") as f:
        f.write(init_text)  # save code init file
    time.sleep(3)
    os.chdir(cwd) # path_initial
    st.container().empty()

# clear ?



selected_horizontal = option_menu(None, ["Home", "New", "Load", 'Save'],
                                  icons=['house', 'plus-square', 'bi-file-earmark-arrow-down-fill',
                                         'bi-file-earmark-arrow-up-fill',
                                         ],
                                  menu_icon="cast", default_index=0, orientation="horizontal",
                                  styles={
                                      "container": {"padding": "0!important", "background-color": "#fafafa"},
                                      "icon": {"color": "orange", "font-size": "25px"},
                                      "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                                                   "--hover-color": "#eee"},
                                      "nav-link-selected": {"background-color": "green"},
                                  }
                                  )
selected_node = []
data_code = ""
if selected_horizontal == 'Load':
    loaded_file = st.file_uploader("Choose a file")
    if loaded_file:
        bytes_data = loaded_file.getvalue()
        data_code = loaded_file.getvalue().decode('utf-8')

        code_editeur = st_ace(value=data_code, language='forth', theme='cobalt', font_size=25, key=loaded_file.name)

if selected_horizontal == 'Save':
    saved_file = st.file_uploader("Choose a file")
    saved_file = data_code

if selected_horizontal == 'New':
    code_editeur = st_ace(value=f"node {node}\n", language='forth', theme='cobalt', font_size=25, key=f"{node}.ga")
    if st.button:  # CTRL + ENTER
        node_file = f"{code_editeur.title().split()[1]}.ga"  # ['Node','117']  '117.ga'
        st.text(node_file)
        # st.code(code_editeur , language='fortran')
        with open(node_file, "w") as f:
            f.write(code_editeur)  # save code to '117.ga'

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

my_expander = st.expander(label='GA144 Nodes')
with my_expander:
    list_node_button = [

        "700", "701", "702", "703", "704", "705", "706", "707", "708", "709", "710", "711", "712", "713", "714", "715",
        "716", "717",
        "600", "601", "602", "603", "604", "605", "606", "607", "608", "609", "610", "611", "612", "613", "614", "615",
        "616", "617",
        "500", "501", "502", "503", "504", "505", "506", "507", "508", "509", "510", "511", "512", "513", "514", "515",
        "516", "517",
        "400", "401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415",
        "416", "417",
        "300", "301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315",
        "316", "317",
        "200", "201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212", "213", "214", "215",
        "216", "217",
        "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115",
        "116", "117",
        "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
        "016", "017"
    ]

    cols = cycle(st.columns(18))  # st.columns here since it is out of beta at the time I'm writing this
    for idx, button_node in enumerate(list_node_button):
        next(cols).button(label=str(button_node))
