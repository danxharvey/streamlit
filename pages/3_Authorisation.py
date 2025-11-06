# Import libraries
import streamlit as st
from components.footer import show_footer
from components.sidebar import show_sidebar
from components.header import show_header


# ---- Sidebar ----
show_sidebar()

# ---- Header ----
show_header(page_title='Neuron 5 - Authorisation',
            title = 'Authorisation Module',
            subtitle = 'Neuron 5 custom authorisation module for FastAPI backend.')

# ---- Auth Form ----
st.header('User Login', divider='red')
with st.form('auth_form', clear_on_submit=False):
    st.subheader(':red[Backend not yet connected]')
    username = st.text_input('Username', placeholder='Enter your username')
    password = st.text_input('Password', type='password', placeholder='Enter your password')
    login_btn = st.form_submit_button('Login')

    # ---- Login Handling ----
    if login_btn:
        # Placeholder for FastAPI backend validation
        if username == '' or password == '':
            st.warning('Please enter both username and password')
        else:
            # Example: pretend backend response
            user_exists = True  # Replace with backend check
            pw_correct = True   # Replace with backend check

            if user_exists and pw_correct:
                st.success(f'Welcome back, {username}!')
            elif not user_exists:
                st.error('Username does not exist')
            else:
                st.error('Password is incorrect')

    # ---- Reset Password Handling ----
    with st.expander('Forgot password?'):
        new_pw = st.text_input('New password', type='password', placeholder='Enter new password')
        confirm_pw = st.text_input('Confirm new password', type='password', placeholder='Confirm password')
        submit_reset = st.form_submit_button('Update Password')
        
        if submit_reset:
            if new_pw != confirm_pw:
                st.error('Passwords do not match!')
            elif len(new_pw) < 6:
                st.warning('Password should be at least 6 characters')
            else:
                # Placeholder for FastAPI password update
                st.success('Password successfully updated!')

# ---- Footer ----
show_footer()