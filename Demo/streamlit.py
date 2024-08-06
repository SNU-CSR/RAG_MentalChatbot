<<<<<<< HEAD
import streamlit as st
import google.generativeai as genai

st.title("Mental chat bot")

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-pro')
    print("model loaded...")
    return model

model = load_model()

# session_state : 객체 활용해 대화 이력을 세션으로 관리
# 사용자와 ai의 메시지 생성될 때마다 대화 이력에 메시지 정보 추가
if "chat_session" not in st.session_state:
    st.session_state["chat_session"] = model.start_chat(history=[])
    
# 대화 이력에 추가된 메시지는 사용자 인터랙션 있을때마다
# for loop으로 메시지 전체가 화면으로 출력되도록 함 
for content in st.session_state.chat_session.history:
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)
    
if prompt := st.chat_input("메시지를 입력하세요. "):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)       
=======
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
>>>>>>> origin/develop
