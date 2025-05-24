import streamlit as st

from dotenv import load_dotenv
from utils.session import session_control

load_dotenv()
session_control()

st.title("PERPLEXITY")
st.markdown(
    "LLM에 **웹검색 기능**을 추가한 PerPlexity클론 프로젝트 입니다.웹서치, 멀티턴대화를 지원합니다."
)

# 사이드바
with st.sidebar:
    # 초기화 버튼
    clear_btn = st.button("대화 초기화")

    st.markdown("# **made by JDJ**")

    # 모델 선택
    selected_model = st.selectbox(
        "LLM선택", ["gpt-4o", "gpt-4o-mini", "정대진"], index=0
    )

    # 검색 결과 개수 설정
    search_model = st.slider("검색결과", min_value=1, max_value=10, value=3)

    # include_domains 설정
    st.subheader("검색 도메인 설정")
    search_topic = st.selectbox("검색 주제", ["general", "news"], index=0)
    new_domain = st.text_input("추가할 도메인 입력")
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("도메인 추가", key="add_domain"):
            if new_domain and new_domain not in st.session_state["include_domains"]:
                st.session_state["include_domains"].append(new_domain)

    # 현재 등록된 도메인 목록 표시
    st.write("등록된 도메인 목록:")
    for idx, domain in enumerate(st.session_state["include_domains"]):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text(domain)
        with col2:
            if st.button("삭제", key=f"del_{idx}"):
                st.session_state["include_domains"].pop(idx)
                st.rerun()

    # 설정 버튼
    apply_btn = st.button("설정 완료", type="primary")
# 사용자 입력
user_input = st.chat_input("궁금한 내용을 물어보세요")

# 경고메시지를 띄우기 위한 빈 영역
warning_msg = st.empty()
