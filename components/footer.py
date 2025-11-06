# components/footer.py
import streamlit as st
from datetime import datetime

def show_footer():
    current_year = datetime.now().year
    st.write('---')
    st.caption(f'© {current_year} Neuron 5. All rights reserved.')
