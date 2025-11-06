import streamlit as st

def show_sidebar(user_logged_in=None):
    # ---- Example Session State ----
    if user_logged_in not in st.session_state:
        st.session_state.user = 'Peter Parker'  # replace with login info

        # ---- Sidebar Template ----
        with st.sidebar:
            st.logo('img/favicon.ico', size="large", link=None, icon_image=None)
            # Welcome Section
            st.markdown(f'## :wave: Welcome, {st.session_state.user}!')
            st.divider()
            
            # Logout button
            if st.button('Logout'):
                st.error('To Be Completed')
                st.session_state.user = None
                st.experimental_rerun()