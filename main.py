import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

def get_api_key():
    return os.getenv("API_KEY")

def main():
    if "visible" not in st.session_state:
        st.session_state["visible"] = False

    if "apiToast" not in st.session_state:
        st.session_state["apiToast"] = False

    if os.path.exists(".env"):
        with open(".env", "r") as f:
            os.environ["API_KEY"] = f.readline().split("=")[1].strip()
            f.close()

    if get_api_key():
        st.switch_page("pages/home.py")
    else:
        st.switch_page("pages/api_key.py")

if __name__ == "__main__":
    main()

# st.switch_page("pages/1_Home.py")