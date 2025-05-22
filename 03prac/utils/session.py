import streamlit as st

def session_control():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    if "react_agent" not in st.session_state:
        st.session_state["react_agent"]= []

    if "include_domains" not in st.session_state:
        st.session_state["include_domains"] = []