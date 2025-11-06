# Import libraries
import streamlit as st
import pandas as pd
from components.footer import show_footer
from components.sidebar import show_sidebar
from components.header import show_header


# ---- Sidebar ----
show_sidebar()

# ---- Header ----
show_header(page_title='Neuron 5 - Home',
            title = 'Purpose of Codebase',
            subtitle = 'Deployable testing hub for work samples and product development ideas.')

# ---- Main content -----
st.header('What is currently planned?', divider='red')

# Load plans array from json
df = pd.read_json('data/plans.json')

# Display in columns for visual appeal
cols = st.columns(2)
for i, (_, plan) in enumerate(df.iterrows()):
    col = cols[i % 2]
    with col:
        st.markdown(f"""
        <div style="
            padding: 15px; 
            border-radius: 10px;
            color:#000000; 
            background-color:#e0f7fa;  /* light background */
            margin-bottom:10px;
            border: 1px solid #b2ebf2;
        ">
            <h4 style="margin:0">{plan['emoji']} {plan['title']}</h4>
            <p style="color:#333; margin-top:5px">{plan['description']}</p>
        </div>
        """, unsafe_allow_html=True)

# ---- Footer ----
show_footer()