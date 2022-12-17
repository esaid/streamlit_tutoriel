import json
import os
import time
import glob

import requests
import serial.tools.list_ports
import streamlit as st
from streamlit_ace import st_ace
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from itertools import cycle


# lottie url file
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def file_in_folder():
    dir = "\n\r".join(str(st.session_state['folder_project']).splitlines())
    os.chdir(dir)  # path projet
    return sorted(glob.glob("*.ga"))


# gestion projet
if 'projet' not in st.session_state:
    st.session_state['projet'] = False

if 'name_projet' not in st.session_state:
    st.session_state['name_projet'] = ""

# gestion repertoire projet
if 'folder_project' not in st.session_state:
    st.session_state['folder_project'] = ''
# gestion repertoire streamlit
if 'folder_streamlit' not in st.session_state:
    st.session_state['folder_streamlit'] = "\n\r".join(os.getcwd().splitlines())  # sauvegarde repertoire streamlit

if 'code' not in st.session_state:
    st.session_state['code'] = ''


if 'file_node' not in st.session_state:
    st.session_state['file_node'] = ''

# elargir la page
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# charger animation cpu
cpu_file = "cpu.json"
dir_cpu_file = f"{st.session_state['folder_streamlit']}\{cpu_file}"
os.chdir(st.session_state['folder_streamlit'])  # path streamlit
st.write(os.getcwd())
# lottie_cpu = load_lottiefile(cpu_file)

# charger animation ecriture code informatique
lottie_urlGA144 = "https://assets9.lottiefiles.com/packages/lf20_xafe7wbh.json"
lottie_jsonGA144 = load_lottieurl(lottie_urlGA144)

# titre avec style css html
original_title = '<p style="font-family:Courier; color:Green; font-size: 40px;">GA144 FORTH</p>'
st.markdown(original_title, unsafe_allow_html=True)
# affichage repertoire fichiers du projet si exisant
if st.session_state['projet'] is True:
    st.write(f"Projet ::  {st.session_state['name_projet']}\n")
    for files in file_in_folder():
        st.write(f"\n ---->  {files}")
# afficher  animation cpu
with st.spinner(text="GA144"):
    st_lottie(lottie_jsonGA144, height=150, key="loading_gif")
# afficher animation cpu et menu vertical
with st.sidebar:
    # st_lottie(lottie_cpu, speed=1, height=150)
    selected_vertical_menu = option_menu("Main Menu", ["Home", 'Settings', 'About'], icons=['house', 'gear'],
                                         menu_icon="cast",
                                         default_index=0)
    # selection node par type et numero node
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

# col2 creation ou col1 ouvrir un projet le fichier ini.ga ( pour connaitre le repertoire )
col1, col2 = st.columns([1, 1])
# charger  projet
with col1:
    placeholder_col1 = st.empty()  # permet de faire disparaitre les elements
    with placeholder_col1.container():
        # si pas de projet , on sélectionne le repertoire et fichier ini.ga
        if st.session_state['projet'] is False:
            st.title('Load Project :')
            select_projet = st.file_uploader("Choose a file init.ga in project folder ", type=['ga'])

            st.warning('Please select a file init.ga')

            if select_projet:
                if select_projet.name == 'init.ga':
                    st.info("file init.ga' selected")

                    st.session_state['projet'] = True
                    directory_project = select_projet.getvalue().decode('utf-8')[2:]  # chemin du projet
                    st.session_state['folder_project'] = directory_project
                    name_projet = directory_project[directory_project.rindex('/') + 1:]
                    st.session_state['name_projet'] = name_projet
                    # st.write(name_projet)
                    # st.write(file_in_folder())
                    time.sleep(4)
                    placeholder_col1.empty().empty()  # on fait disparaitre les elements

# creer projet
with col2:
    placeholder_col2 = st.empty()  # permet de faire disparaitre les elements
    with placeholder_col2.container():
        # si pas de projet  , creation du projet
        if st.session_state['projet'] is False:
            st.title('Create Project :')

            name_projet = st.text_input('Name Project :  👇')  # nom du projet
            # st.write(f"Current working directory: {st.session_state['folder_streamlit']}")  # folder courant
            if not name_projet:  # gere si on a bien rentrer un nom de projet
                st.warning('Please input a name directory project')
                st.stop()
            st.session_state['projet'] = True
            st.session_state['name_projet'] = name_projet
            st.success(f"Thank you for inputting a name. {st.session_state['projet']}")
            st.session_state['folder_project'] = os.path.join(st.session_state['folder_streamlit'],
                                                              name_projet)  # chemin repertoire du projet
            try:
                os.mkdir(st.session_state['folder_project'])  # creation repertoire , avec nom de projet
            except OSError as errordirectory:
                st.error(f'This is an error  {errordirectory}', icon="🚨")
                st.stop()
            os.chdir(rf"{st.session_state['folder_project']}")  # path projet
            st.info(f'Create init.ga file in {name_projet}', icon="ℹ️")
            init_text = f"/ {st.session_state['folder_project']}\n"  #
            # creation du fichier ini.ga
            with open('init.ga', "w") as f:
                f.write(init_text)  # save code init file

            # os.chdir ( st.session_state['folder_streamlit'] )  # path_initial

            st.write(os.getcwd())
            st.write(file_in_folder())
            time.sleep(5)
            placeholder_col2.empty().empty()  # clear
            placeholder_col1.empty().empty()
# menu horizontal
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

if selected_horizontal == 'Home':
    dir = "\n\r".join(str(st.session_state['folder_project']).splitlines())
    st.write(dir)
    os.chdir(dir)  # path projet


def view_code_node():
    code = st.session_state['code']
    # affiche le code dans editeur ace
    code_editeur = st_ace(value=code, language='forth', theme='cobalt', font_size=25, auto_update=True)
    node_file = f"{code_editeur.title().split()[1]}.ga"  # ['Node','117']  '117.ga'
    st.session_state['file_code'] = node_file
    st.session_state['code'] = code_editeur



# charger fichier *.ga
if selected_horizontal == 'Load':
    dir = "\n\r".join(str(st.session_state['folder_project']).splitlines())
    st.write(dir)
    os.chdir(dir)  # path projet
    loaded_file = st.file_uploader("Choose a file", type='ga')
    if loaded_file:
        st.session_state['code'] = loaded_file.getvalue().decode('utf-8')
        st.write(st.session_state['code'])
        view_code_node()


if selected_horizontal == 'Save':
    file_save = st.session_state['file_code']
    file_code = st.session_state['code']
    with open(file_save, "w") as f:
        f.write(file_code)  # save code init file
        st.write('save')
    view_code_node()

if selected_horizontal == 'New':
    code_editeur = st_ace(value=f"node {node}\n", language='forth', theme='cobalt', font_size=25, auto_update=True)
    node_file = f"{code_editeur.title().split()[1]}.ga"  # ['Node','117']  '117.ga'
    folder_file = f"{st.session_state['folder_project']}/{node_file}".strip()
    st.text(f"Node : {folder_file}")
    time.sleep(5)
    dir = "\n\r".join(str(st.session_state['folder_project']).splitlines())
    st.write(dir)
    os.chdir(dir)  # path projet
    with open(node_file, "w") as f:  # sauvegarde dans le repertoire projet le fichier node.ga
        f.write(code_editeur)  # save code to '117.ga'
    time.sleep(5)
    st.session_state['file_code'] = node_file
    st.session_state['code'] = code_editeur


if selected_vertical_menu == 'About':
    st.info('informational message GA144 program ', icon="ℹ️")

# gestion port serie
if selected_vertical_menu == 'Settings':
    message = ''
    ports = serial.tools.list_ports.comports()
    list_port = []
    for port, desc, hwid in sorted(ports):
        list_port.append(port)
    option_port_serial = st.selectbox('Serial Port selection', list_port)
    st.write('You selected:', option_port_serial)

# gestion GA144 nodes
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
