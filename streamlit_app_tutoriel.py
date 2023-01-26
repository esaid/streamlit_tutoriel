import time
import json
import streamlit as st
from streamlit_lottie import st_lottie
from contextlib import redirect_stdout, redirect_stderr
import io
import sys
import subprocess
import traceback
import streamlit as st
import pandas as pd

st.set_page_config ( layout='wide' )
st.header ( " UN TITRE " )


def load_lottiefile(filepath: str):
    with open ( filepath, "r" ) as f:
        return json.load ( f )


cpu_file = "cpu.json"
lottie_coding = load_lottiefile ( cpu_file )

st_lottie ( lottie_coding, speed=1, height=200 )

st.write ( "Hello ,let's learn how to build a streamlit app together" )
st.title ( "this is the app title" )
st.markdown ( "## this is the markdown" )
st.header ( "this is the header" )
st.subheader ( "this is the subheader" )
st.caption ( "this is the caption" )
st.code ( "x=2021" , language="python")
st.latex ( r''' a+a r^1+a r^2+a r^3 ''' )
st.checkbox ( 'yes' )
st.button ( 'Click' )
st.radio ( 'Pick your gender', ['Male', 'Female'] )
st.selectbox ( 'Pick your gender', ['Male', 'Female'] )
st.multiselect ( 'choose a planet', ['Jupiter', 'Mars', 'neptune'] )
st.select_slider ( 'Pick a mark', ['Bad', 'Good', 'Excellent'] )
st.slider ( 'Pick a number', 0, 60 )

st.number_input ( 'Pick a number', 0, 10 )
st.text_input ( 'Email address' )
st.date_input ( 'Travelling date' )
st.time_input ( 'School time' )
st.text_area ( 'Description' )
st.file_uploader ( 'Upload a photo' )
st.color_picker ( 'Choose your favorite color' )

st.progress ( 10 )
with st.spinner ( 'Wait for it...' ):
    time.sleep ( 4 )

st.graphviz_chart ( '''
    digraph {
        Nicolas -> Jean
        Maman -> Fils
        Maman -> Fille
        Sophie -> Pierre
    }
''' )

st.header ( "Left: Body, Middle: Std Out, Right: Std Err" )
body, stdout, stderr = st.columns ( 3 )  # 3 colonnes Gauche Milieu Droite

# dataframe
df = pd.DataFrame ( {"test": [1, 2, 3]} )
st.write ( f"information panda dataframe :  {df}" )
button = body.button ( 'wtf' )  # un bouton
body.write ( df )  # affiche le dataframe

# redirige vers une console dans la page streamlit
with redirect_stdout ( io.StringIO () ) as stdout_f, redirect_stderr ( io.StringIO () ) as stderr_f:
    try:
        print ( 'Hello World!' )
        x = 1 / 0
    except Exception as e:
        traceback.print_exc ()
        traceback.print_exc ( file=sys.stdout )  # or sys.stdout

stdout_text = stdout_f.getvalue ()
stdout.text ( stdout_text )
stderr_text = stderr_f.getvalue ()
stderr.text ( stderr_text )


if st.button(" Ballons "):
    st.balloons()