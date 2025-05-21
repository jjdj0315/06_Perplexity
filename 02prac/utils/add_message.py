import streamlit as st
from langchain_core.messages import ChatMessage
from utils.dataclass import ChatMessageWithType
from utils.handler import format_search_result

def add_message(role, message, msg_type="text", tool_name=""):
    if msg_type == "text":
        st.session_state["messages"].append(
            ChatMessageWithType(
                chat_message=ChatMessage(role=role, content=message),
                msg_type="text",
                tool_name=tool_name,
            )
        )
    elif msg_type == "tool_result":
        st.session_state["messages"].append(
            ChatMessageWithType(
                chat_message=ChatMessage(
                    role="assistant", content=format_search_result(message)
                ),
                msg_type="tool_result",
                tool_name=tool_name,
            )
        )