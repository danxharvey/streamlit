# Import libraries
import streamlit as st
import pydeck as pdk
import pandas as pd

# Neuron 5 logo
st.logo('img/favicon.ico', size='large', link=None, icon_image=None)
st.image('img/bg_logo.png', width=400)

# Describe page
st.title(':blue[Purpose of Codebase]')
st.markdown('**Deployable testing hub for work samples and product development ideas.**')

# Gather user inputs
st.write('&nbsp;')
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