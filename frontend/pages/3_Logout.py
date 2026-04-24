import streamlit as st

st.set_page_config(page_title="Logout", page_icon="👋")

# Clear session state
st.session_state.token = None
st.session_state.email = None
st.session_state.allergy = None

# Clear all other session state keys
for key in list(st.session_state.keys()):
    if key not in ['token', 'email', 'allergy']:
        del st.session_state[key]

# Redirect to home
st.switch_page("Home.py")