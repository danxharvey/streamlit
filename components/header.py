# components/header.py
import streamlit as st

def show_header(page_title: str, title: str, subtitle: str = ''):
    st.set_page_config(page_title=page_title, page_icon='img/favicon.ico', layout='centered')
    st.image('img/bg_logo.png', width=400)  # consistent branding
    st.title(f':blue[{title}]')
    if subtitle:
        st.markdown('**' + subtitle + '**')
    st.write('---')
