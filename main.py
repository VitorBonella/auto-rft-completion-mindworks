import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import hmac

def get_api_key():
    return os.getenv("API_KEY")

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


def main():
    

    if "visible" not in st.session_state:
        st.session_state["visible"] = False

    if "apiToast" not in st.session_state:
        st.session_state["apiToast"] = False

    if not check_password():
        st.stop() 

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