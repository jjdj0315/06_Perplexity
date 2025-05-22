
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from dotenv import load_dotenv

from utils.session import session_control
from utils.uuid import random_uuid
from utils.print_message import print_messages
from utils.tools import WebSearchTool
from utils.agent import create_agent_executor
from utils.handler import stream_handler
from utils.add_message import add_message

session_control()
load_dotenv()

st.title("Perplexity")
st.markdown("LLM에 **웹검색 기능**을 추가한 PerPlexity클론 프로젝트 입니다.웹서치, 멀티턴대화를 지원합니다.")

# 대화기록을 저장하기 위한 용도로 생성
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ReAct Agent 초기화
if "react_agent" not in st.session_state:
    st.session_state["react_agent"] = None

# include_domains 초기화
if "include_domains" not in st.session_state:
    st.session_state["include_domains"] = []
    
#사이드바 생성
with st.sidebar:
    #초기화 버튼
    clear_btn = st.button("대화 초기화")
    
    st.markdown("# **made by JDJ**")
    
    #모델 선택
    selected_model = st.selectbox("LLM 선택", ["gpt-4o", "gpt-4o-mini","정대진"], index = 0)

    #검색 결과 개수 설정
    search_result_count = st.slider("검색 결과", min_value=1, max_value=10, value=3)
    
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
    

#초기화 버튼
if clear_btn:
    st.session_state["messages"] = []
    st.session_state["thread_id"] = random_uuid()

#이전 대화기록출력    
print_messages()

#사용자 입력
user_input = st.chat_input("궁금한 내용을 물어보세요")

#경고메시지를 띄우기 위한 빈 영역
warning_msg = st.empty()

#설정 버튼이 눌리면
if apply_btn:
    tool = WebSearchTool().create()
    tool.max_results = search_result_count
    tool.include_domains = st.session_state['include_domains']
    tool.topic = search_topic
    st.session_state['react_agent'] = create_agent_executor(
        model_name = selected_model,
        tools = [tool],
    )
    st.session_state['thread_id'] = random_uuid()

#만약에 사용자 입력이 들어오면
if user_input:
    agent = st.session_state['react_agent']
    
    #config설정
    if agent is not None:
        config = {'configurable' : {"thread_id" : st.session_state["thread_id"]}}
        #사용자 입력
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            # 빈 공간(컨테이너)을 만들어서, 여기에 토큰을 스트리밍 출력한다.
            container = st.empty()

            ai_answer = ""
            container_messages, tool_args, agent_answer = stream_handler(
                container,
                agent,
                {
                    "messages": [
                        ("human", user_input),
                    ]
                },
                config,
            )

            # 대화기록을 저장한다.
            add_message("user", user_input)
            for tool_arg in tool_args:
                add_message(
                    "assistant",
                    tool_arg["tool_result"],
                    "tool_result",
                    tool_arg["tool_name"],
                )
            add_message("assistant", agent_answer)
    else:
        warning_msg.warning("사이드바에서 설정을 완료해주세요.")