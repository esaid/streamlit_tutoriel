import bibliotheque_create
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
from contextlib import redirect_stdout, redirect_stderr

import io
import sys
import subprocess
import traceback

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


def bar_progression(progress, t):
    percent_complete = 0
    my_bar = st.progress(percent_complete)
    while percent_complete < 100:
        percent_complete += progress
        time.sleep(t)
        my_bar.progress(percent_complete)
    my_bar.empty()


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


def read_file(name_file):
    with open(name_file, "r") as file_:
        return file_.read()


def concatenation_in_onefile(new_file, list_files):
    with open(new_file, "w") as new_file:
        for name in list_files:
            with open(name) as f:
                for line in f:
                    new_file.write(line)
                new_file.write("\n")


def file_in_folder():
    directory = "\n\r".join(str(st.session_state['folder_project']).split())
    os.chdir(directory)  # path projet
    return sorted(glob.glob("*.node"))


def is_file_exist(file_):
    folder = file_in_folder()
    return file_ + '.node' in folder


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

if 'menu_gestion_projet' not in st.session_state:
    st.session_state['menu_gestion_projet'] = False

# gestion Lib

if 'folder_lib' not in st.session_state:
    st.session_state['folder_lib'] = st.session_state['folder_streamlit'] + "/lib/"

if 'code' not in st.session_state:
    st.session_state['code'] = ''

if 'file_node' not in st.session_state:
    st.session_state['file_node'] = ''

if 'compilation_file' not in st.session_state:
    st.session_state['compilation_file'] = ''

if 'send' not in st.session_state:
    st.session_state['send'] = False

if 'serial_port' not in st.session_state:
    st.session_state['serial_port'] = ''


def select_folder_project():
    project_folder = "\n\r".join(str(st.session_state['folder_project']).split())
    # st.write(project_folder)
    os.chdir(project_folder)  # path projet


def select_folder_streamlit():
    streamlit_folder = "\n\r".join(str(st.session_state['folder_streamlit']).split())
    # st.write(streamlit_folder)
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
st.write(st.session_state['folder_lib'])
# charger animation cpu
cpu_file = "cpu.json"
dir_cpu_file = f"{st.session_state['folder_streamlit']}{cpu_file}"

lottie_cpu = load_lottiefile(cpu_file)

# charger animation ecriture code informatique
lottie_urlGA144 = "https://assets9.lottiefiles.com/packages/lf20_xafe7wbh.json"
lottie_jsonGA144 = load_lottieurl(lottie_urlGA144)

# titre avec style css html
original_title = '<p style="font-family:Courier; color:Green; font-size: 40px;">GA144 FORTH</p>'
st.markdown(original_title, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col3:
    # affichage repertoire fichiers du projet si exisant
    if st.session_state['projet'] is True:
        st.metric("--- Nodes ---", "144", f"{len(file_in_folder()) - 1} nodes")
        st.write('\n')
        project_font = f"""<style>p.a {{ font: bold 15px Courier;}}</style><p class="a">  Project :: {st.session_state['name_projet']}</p>"""
        st.markdown(project_font, unsafe_allow_html=True)
        file_project_font = f"""<style>p.a {{ font: bold 15px Courier;}}</style><p class="a">{', '.join(file_in_folder())}</p>"""
        st.markdown(file_project_font, unsafe_allow_html=True)

# afficher  animation cpu
with st.spinner(text="GA144"):
    st_lottie(lottie_jsonGA144, height=150, key="loading_gif")
# afficher animation cpu et menu vertical
with st.sidebar:
    selected_vertical_menu = option_menu("Main Menu", ["Home", 'Setting-communication', 'About'],
                                         icons=['house', 'motherboard', 'question'],
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
    st_lottie(lottie_cpu, speed=1, height=150)
    selected_horizontal_cpu = option_menu(None, ["", "Compilation", "Send"],
                                          icons=['', 'gear', 'caret-down-square-fill'],
                                          menu_icon="cast", default_index=0, orientation="horizontal",
                                          styles={
                                              "container": {"padding": "0!important", "background-color": "#fafafa"},
                                              "icon": {"color": "orange", "font-size": "18px"},
                                              "nav-link": {"font-size": "18px", "text-align": "left", "margin": "2px",
                                                           "--hover-color": "#eee"},
                                              "nav-link-selected": {"background-color": "green"},
                                          }
                                          )

    if selected_horizontal_cpu == "Compilation":
        st.info(f"compilation {st.session_state['name_projet']}", icon="ℹ️")
        bar_progression(5, 0.1)
        # save name_projet.Cga  (Compilationga)
        l = file_in_folder()
        l = l[-1:] + l[:-1]  # init.node premier element pour gerer  require
        st.session_state['compilation_file'] = st.session_state['name_projet'] + '.Cga'
        concatenation_in_onefile(st.session_state['compilation_file'], l)
        code = read_file(st.session_state['compilation_file'])
        # new code
        file_ga_ = st.session_state['compilation_file'] + '_'
        directoryBibliotheque = st.session_state['folder_lib']
        bibliotheque_create.generation_code(code, directoryBibliotheque, file_ga_)
        st.stop()

    if selected_horizontal_cpu == "Send":
        st.info(f"Send program to board !", icon="ℹ️")
        bar_progression(5, 0.1)
        st.session_state['send'] = True
        st.stop()

col1, col2 = st.columns(2)

# col2 creation ou col1 ouvrir un projet le fichier ini.node ( pour connaitre le repertoire )
# charger  projet

with col1:
    phcol1 = st.empty()
    with phcol1.container():
        # si pas de projet , on sélectionne le repertoire et fichier ini.node
        if st.session_state['projet'] is False:
            st.header('Load Project :')
            select_projet = st.file_uploader("Choose a file init.node in project folder ", type=['node'])
            st.warning('Please select a file init.node')
            if select_projet:
                if select_projet.name == 'init.node':
                    st.info("file init.node' selected")

                    st.session_state['projet'] = True

                    directory_project = select_projet.getvalue().decode('utf-8').split('\n')[0][
                                        2:]  # 1ere ligne , chemin du projet
                    st.session_state['folder_project'] = directory_project
                    name_projet = directory_project[directory_project.rindex('/') + 1:]
                    st.session_state['name_projet'] = name_projet
                    # st.write(name_projet)
                    # st.write(file_in_folder())
                    time.sleep(2)
                    phcol1.empty()

# creer projet
with col2:
    phcol2 = st.empty()
    with phcol2.container():
        # si pas de projet  , creation du projet
        if st.session_state['projet'] is False:
            st.header('Create Project :')
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
            st.info(f'Create init.node file in {name_projet}', icon="ℹ️")
            init_text = f"\ {st.session_state['folder_project']}\n"  #
            # creation du fichier ini.node
            with open('init.node', "w") as f:
                f.write(init_text)  # save code init file
            time.sleep(1)
            phcol1.empty()
            phcol2.empty()
# menu horizontal
selected_horizontal = option_menu(None, ["Home", "New", "Load", 'Save', 'Restart'],
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

if selected_horizontal == 'Restart':
    st.warning('Press F5 or refresh the web page', icon='⚠')

if selected_horizontal == 'Home':
    select_folder_project()


def view_code_node():
    code_ = st.session_state['code']
    # affiche le code dans editeur ace
    code_edit = st_ace(value=code_, language='forth', theme='cobalt', font_size=25, auto_update=True, key='view')
    # node_file = f"{code_editeur.title().split()[1]}.node"  # ['Node','117']  '117.node'
    # st.session_state['file_node'] = node_file
    st.session_state['code'] = code_edit
    return code_edit


# charger fichier *.node
if selected_horizontal == 'Load':
    # select_folder_project()
    loaded_file = st.file_uploader("Choose a file", type='ga')
    if loaded_file:
        st.session_state['file_node'] = loaded_file.name
        # st.write('file : ', st.session_state['file_node'])
        st.session_state['code'] = loaded_file.getvalue().decode('utf-8')
        view_code_node()
        st.stop()

if selected_horizontal == 'Save':
    select_folder_project()
    file_save = st.session_state['file_node']
    # st.write('file : ', st.session_state['file_node'])
    file_code = st.session_state['code']
    # st.write(st.session_state['code'])
    # st.write(file_save)
    with open(file_save, "w") as f:
        f.write(file_code)  # save code init file
        st.info(f'save {file_save}')
        view_code_node()
        st.stop()

if selected_horizontal == 'New':
    if is_file_exist(node):  # node existant ?
        st.warning(f" node {node} exist , please select Load node")
        time.sleep(1)

    else:
        st.session_state['code'] = f"node {node}\n"
        # code_editeur = view_code_node()
        code_editeur = st_ace(value=f"node {node}\n", language='forth', theme='cobalt', font_size=25, auto_update=True,
                              key='new')
        node_file = f"{code_editeur.title().split()[1]}.node"  # ['Node','117']  '117.node'
        folder_file = f"{st.session_state['folder_project']}/{node_file}".strip()
        st.text(f"Node : {folder_file}")
        st.session_state['file_node'] = node_file
        st.session_state['code'] = code_editeur
        st.stop()  # attente save

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
    time.sleep(1)

# gestion GA144 nodes
my_expander = st.expander(label=f"GA144 Nodes {str(file_in_folder()).replace('.node', '').replace('init', '')} ")

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

expander_compilation = st.expander(label=f"GA144 compilation  ")

with expander_compilation:
    if st.session_state['compilation_file']:
        stdout, stderr = st.columns(2)
        with redirect_stdout(io.StringIO()) as stdout_f, redirect_stderr(io.StringIO()) as stderr_f:
            try:
                select_folder_streamlit()
                # ga144compilation_process = subprocess.run(["pwd"], capture_output=True, text=True)
                ga144compilation_process = subprocess.run(
                    ["python", "ga.py", f"{st.session_state['name_projet']}/{st.session_state['name_projet']}.Cga_"],
                    capture_output=True, text=True)
                stdout_f.write(ga144compilation_process.stdout)
                stderr_f.write(ga144compilation_process.stderr)
                # print(read_file(st.session_state['compilation_file']))
                print(read_file(f"{st.session_state['name_projet']}/{st.session_state['compilation_file']}_"))

            except Exception as e:
                traceback.print_exc()
                traceback.print_exc(file=sys.stdout)  # or sys.stdout
        stdout_text = stdout_f.getvalue()
        stdout.text(stdout_text)
        stderr_text = stderr_f.getvalue()
        stderr.text(stderr_text)


expander_send = st.expander(label=f"GA144 send  ")

with expander_send:
    if st.session_state['send']:
        stdout, stderr = st.columns(2)
        with redirect_stdout(io.StringIO()) as stdout_f, redirect_stderr(io.StringIO()) as stderr_f:
            try:
                select_folder_streamlit()
                # ga144send_process = subprocess.run(["pwd"], capture_output=True, text=True)
                ga144send_process = subprocess.run(
                    ["python", "ga.py", f"{st.session_state['name_projet']}/{st.session_state['name_projet']}.Cga_",
                     "--port", f"{st.session_state['serial_port']}"], capture_output=True, text=True)
                stdout_f.write(ga144send_process.stdout)
                stderr_f.write(ga144send_process.stderr)

            except Exception as e:
                traceback.print_exc()
                traceback.print_exc(file=sys.stdout)  # or sys.stdout
        stdout_text = stdout_f.getvalue()
        stdout.text(stdout_text)
        stderr_text = stderr_f.getvalue()
        stderr.text(stderr_text)
        st.session_state['send'] = False
        st.write('end send')
