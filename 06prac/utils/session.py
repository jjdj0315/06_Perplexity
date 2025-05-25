# session
import streamlit as st


def session_control():
    # 대화기록을 저장하기 위한 용도로 생성
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # ReAct Agent 초기화
    if "react_agent" not in st.session_state:
        st.session_state["react_agent"] = None

    # include_domains 초기화
    if "include_domains" not in st.session_state:
        st.session_state["include_domains"] = []
