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
st.set_page_config(layout='wide')

st.header("Left: Body, Middle: Std Out, Right: Std Err")
body, stdout, stderr = st.columns(3)

with redirect_stdout(io.StringIO()) as stdout_f, redirect_stderr(io.StringIO()) as stderr_f:
    try:
        print('Hello World!')
        df = pd.DataFrame({"test": [1,2,3]})
        df.info()
        good_process = subprocess.run(["ls", "-lah", "."], capture_output=True, text=True)
        good_process = subprocess.run(["python", "--version"], capture_output=True, text=True)
        stdout_f.write(good_process.stdout)
        stderr_f.write(good_process.stderr)
        bad_process = subprocess.run(["ls", "wtf"], capture_output=True, text=True)  # Throws stderr error
        stdout_f.write(bad_process.stdout)
        stdout_f.write(bad_process.stderr) # Also print in in middle column (most of my usecases i like stdout and stderr)

        x = 1 / 0 # Throws Python Error

    except Exception as e:
        traceback.print_exc()
        traceback.print_exc(file=sys.stdout) # or sys.stdout
button = body.button('wtf')
if button:
    # Outisde of context, doesn't display in streamlit
    print('BUTTON')
body.write(df)
stdout_text = stdout_f.getvalue()
stdout.text(stdout_text)
stderr_text = stderr_f.getvalue()
stderr.text(stderr_text)

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


cpu_file = "cpu.json"
lottie_coding = load_lottiefile(cpu_file)

st_lottie(lottie_coding, speed= 1, height=200)


st.write("Hello ,let's learn how to build a streamlit app together")
st.title ("this is the app title")
st.header("this is the markdown")
st.markdown("this is the header")
st.subheader("this is the subheader")
st.caption("this is the caption")
st.code("x=2021")
st.latex(r''' a+a r^1+a r^2+a r^3 ''')
st.checkbox('yes')
st.button('Click')
st.radio('Pick your gender',['Male','Female'])
st.selectbox('Pick your gender',['Male','Female'])
st.multiselect('choose a planet',['Jupiter', 'Mars', 'neptune'])
st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
st.slider('Pick a number', 0,60)

st.number_input('Pick a number', 0,10)
st.text_input('Email address')
st.date_input('Travelling date')
st.time_input('School time')
st.text_area('Description')
st.file_uploader('Upload a photo')
st.color_picker('Choose your favorite color')

st.balloons()
st.progress(10)
with st.spinner('Wait for it...'):
    time.sleep(10)


st.graphviz_chart('''
    digraph {
        Big_shark -> Tuna
        Tuna -> Mackerel
        Mackerel -> Small_fishes
        Small_fishes -> Shrimp
    }
''')

