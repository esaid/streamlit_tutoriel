import json
import streamlit as st
import streamlit_lottie as st_lottie


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


cpu_file = "cpu.json"
lottie_coding = load_lottiefile(cpu_file)
st.title("CPU GA144")
st_lottie.st_lottie(lottie_coding)
