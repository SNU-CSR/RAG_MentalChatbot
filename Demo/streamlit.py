import sys
import os

# 현재 파일의 디렉토리 경로를 얻고 부모 디렉토리를 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import streamlit as st
from IntegrationChat import chatbot_response

# Streamlit 설정
st.header("🤖 Mental Health Chatbot")

user_input = st.text_input("당신의 질문을 입력하세요:")

if st.button("전송"):
    response = chatbot_response(user_input)
    st.write("챗봇의 응답:")
    st.write(response)
