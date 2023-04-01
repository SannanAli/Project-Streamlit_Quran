import streamlit as st
import streamlit.components.v1 as stc
from app_singleverse import *
from app_multiverse import *


def main():
    st.title("Holy Quran")
    stc.html(HTML_BANNER)
    menu = ["Home", "Multiverse", "About"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        run_singleverse()
    elif choice == "Multiverse":
        run_multiverse()
    else:
        st.title("Made By Sannan Ali")
        st.subheader("Made with Streamlit")
        st.text("@SANNNA_ALI")


if __name__ == "__main__":
    main()
