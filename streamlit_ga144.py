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

GPIO = ('600', '500', '217', '317', '417', '517', '715')
Analog = ('117', '617', '717', '713', '709')

CLK = ('300', '001', '701')
DATA = ('300', '001', '701')
Internal = (
    '002', '003', '004', '005', '006', '010', '011', '012', '013', '014', '015', '016', '017', '101', '102', '103',
    '104', '105', '106', '107',
    '108', '109', '110', '111', '112', '113', '114', '115', '116', '201', '202', '203', '204', '205', '206', '207',
    '208', '209', '210', '211', '212',
    '213', '214', '215', '216', '300', '301', '302', '303', '304', '305', '306', '307', '308', '309', '310', '311',
    '312', '313', '314', '315', '316',
    '400', '401', '402', '403', '404', '405', '406', '407', '408', '409', '410', '411', '412', '413', '414', '415',
    '416',
    '501', '502', '503', '504', '505', '506', '507', '508', '509', '510', '511', '512', '513', '514', '515', '516',
    '601', '602', '603', '604', '605', '606', '607', '608', '609', '610', '611', '612', '613', '614', '615', '616',
    '700', '701', '702', '703', '704', '706', '707', '708', '710', '711', '712', '714', '716')


def find_fonction_node(node_):
    if node_ in GPIO:
        return 'GPIO'
    if node_ in Analog:
        return 'Analog'
    if node_ in CLK:
        return 'CLK'
    if node_ in DATA:
        return 'DATA'
    if node_ in Internal:
        return 'Internal'


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
    directory = "\n\r".join(str(st.session_state['folder_project']).splitlines())
    os.chdir(directory)  # path projet
    return sorted(glob.glob("*.ga"))


def is_file_exist(file_):
    folder = file_in_folder()
    return file_ + '.ga' in folder


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
    # initialisation par defaut
    st.session_state['folder_streamlit'] = os.path.dirname(__file__)  # sauvegarde repertoire streamlit

if 'folder_principal' not in st.session_state:
    st.session_state['folder_principal'] = st.session_state['folder_streamlit']

if 'code' not in st.session_state:
    st.session_state['code'] = ''

if 'file_node' not in st.session_state:
    st.session_state['file_node'] = ''

if 'serial_port' not in st.session_state:
    st.session_state['serial_port'] = ''


def select_folder_project():
    project_folder = "\n\r".join(str(st.session_state['folder_project']).splitlines())
    st.write(project_folder)
    os.chdir(project_folder)  # path projet


def select_folder_streamlit():
    streamlit_folder = "\n\r".join(str(st.session_state['folder_streamlit']).splitlines())
    st.write(streamlit_folder)
    os.chdir(streamlit_folder)  # path projet


def select_Folder_principal():
    if os.path.exists(master_folder):
        st.session_state['folder_principal'] = master_folder
        st.success("Folder validated ")
        time.sleep(4)
    else:
        st.warning('error Folder not found...')
        st.stop()


def file_exist(file_):
    return os.path.exists(file_) and os.stat(file_).st_size == 0


# élargir la page
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

select_folder_streamlit()
# charger animation cpu
cpu_file = "cpu.json"
dir_cpu_file = f"{st.session_state['folder_streamlit']}\{cpu_file}"

lottie_cpu = load_lottiefile(cpu_file)

# charger animation ecriture code informatique
lottie_urlGA144 = "https://assets9.lottiefiles.com/packages/lf20_xafe7wbh.json"
lottie_jsonGA144 = load_lottieurl(lottie_urlGA144)

col1, col2, col3 = st.columns([1, 1, 1])

# titre avec style css html
original_title = '<p style="font-family:Courier; color:Green; font-size: 40px;">GA144 FORTH</p>'
st.markdown(original_title, unsafe_allow_html=True)
with col3:
    # affichage repertoire fichiers du projet si exisant
    if st.session_state['projet'] is True:
        project_font = f"""<style>p.a {{ font: bold 15px Courier;}}</style><p class="a">Project :: {st.session_state['name_projet']}</p>"""
        st.markdown(project_font, unsafe_allow_html=True)
        file_project_font = f"""<style>p.a {{ font: bold 15px Courier;}}</style><p class="a">{', '.join(file_in_folder())}</p>"""
        st.markdown(file_project_font, unsafe_allow_html=True)


# afficher  animation cpu
with st.spinner(text="GA144"):
    st_lottie(lottie_jsonGA144, height=150, key="loading_gif")
# afficher animation cpu et menu vertical
with st.sidebar:
    st_lottie(lottie_cpu, speed=1, height=150)
    selected_vertical_menu = option_menu("Main Menu", ["Home", 'Setting-communication', 'About'],
                                         icons=['house', 'gear'],
                                         menu_icon="cast",
                                         default_index=0)
    # selection node par type et numero node

    node_type = st.selectbox(
        'Node Type Selection :',
        ('NODE', 'GPIO', 'Analog_In', 'Analog_Out', 'CLK', 'DATA', 'Internal'))

    list_node = ''
    if node_type == 'GPIO':
        list_node = GPIO
    if node_type == 'Analog_In':
        list_node = Analog
    if node_type == 'Analog_Out':
        list_node = Analog
    if node_type == 'CLK':
        list_node = CLK
    if node_type == 'DATA':
        list_node = DATA
    if node_type == 'Internal':
        list_node = Internal

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
            if not name_projet:  # gere si on a bien rentre un nom de projet
                st.warning('Please input a name  project')
                st.stop()
            master_folder = st.text_input(label='Input Master Folder for projects :  📗   ',
                                          help=st.session_state['folder_principal'])
            if not master_folder:
                st.warning('Please input a Folder')
                st.stop()
            select_Folder_principal()
            st.write(f"Current working directory: {st.session_state['folder_streamlit']}")  # folder courant

            st.session_state['projet'] = True
            st.session_state['name_projet'] = name_projet
            st.success(f"Thank you for inputting a name. {st.session_state['projet']}")
            st.session_state['folder_project'] = os.path.join(st.session_state['folder_principal'],
                                                              name_projet)  # chemin repertoire du projet
            try:
                os.mkdir(st.session_state['folder_project'])  # creation repertoire , avec nom de projet
            except OSError as errordirectory:
                st.error(f'This is an error  {errordirectory}', icon="🚨")
                st.stop()
            select_folder_project()
            st.info(f'Create init.ga file in {name_projet}', icon="ℹ️")
            init_text = f"/ {st.session_state['folder_project']}\n"  #
            # creation du fichier ini.ga
            with open('init.ga', "w") as f:
                f.write(init_text)  # save code init file
            time.sleep(1)
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

if selected_horizontal == 'Home':
    select_folder_project()


def view_code_node():
    code = st.session_state['code']
    # affiche le code dans editeur ace
    code_editeur = st_ace(value=code, language='forth', theme='cobalt', font_size=25, auto_update=True)
    node_file = f"{code_editeur.title().split()[1]}.ga"  # ['Node','117']  '117.ga'
    st.session_state['file_node'] = node_file
    st.session_state['code'] = code_editeur


# charger fichier *.ga
if selected_horizontal == 'Load':
    select_folder_project()
    loaded_file = st.file_uploader("Choose a file", type='ga')
    if loaded_file:
        st.session_state['code'] = loaded_file.getvalue().decode('utf-8')
        st.write(st.session_state['code'])
        view_code_node()

if selected_horizontal == 'Save':
    select_folder_project()
    file_save = st.session_state['file_node']
    file_code = st.session_state['code']
    if file_save:
        with open(file_save, "w") as f:
            f.write(file_code)  # save code init file
            st.info(f'save {file_save}')
        view_code_node()
    else:
        st.warning('no file selected')

if selected_horizontal == 'New':
    if is_file_exist(node):
        st.warning(" node exist , please select Load node")
        time.sleep(4)
    else:
        code_editeur = st_ace(value=f"node {node}\n", language='forth', theme='cobalt', font_size=25, auto_update=True)
        node_file = f"{code_editeur.title().split()[1]}.ga"  # ['Node','117']  '117.ga'
        folder_file = f"{st.session_state['folder_project']}/{node_file}".strip()
        st.text(f"Node : {folder_file}")
        time.sleep(5)
        select_folder_project()
        with open(node_file, "w") as f:  # sauvegarde dans le repertoire projet le fichier node.ga
            f.write(code_editeur)  # save code to '117.ga'
        time.sleep(1)
        st.session_state['file_node'] = node_file
        st.session_state['code'] = code_editeur

if selected_vertical_menu == 'About':
    st.info('informational message GA144 program ', icon="ℹ️")

# gestion port serie
if selected_vertical_menu == 'Setting-communication':
    message = ''
    ports = serial.tools.list_ports.comports()
    list_port = []
    for port, desc, hwid in sorted(ports):
        list_port.append(port)
    option_port_serial = st.selectbox('Serial Port selection', list_port)
    st.write('You selected:', option_port_serial)
    st.session_state['serial_port'] = option_port_serial

# gestion GA144 nodes
my_expander = st.expander(label=f"GA144 Nodes {str(file_in_folder()).replace('.ga', '').replace('init', '')} ")

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
        if button_node in str(file_in_folder()):  # find nodes
            type_ = 'primary'
            help_ = find_fonction_node(button_node)
        else:
            type_ = 'secondary'
            help_ = ''
        next(cols).button(label=str(button_node), type=type_, help=help_)
