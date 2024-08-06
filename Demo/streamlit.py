# streamlit_app.py

import sys
import os

# 현재 파일의 디렉토리 경로를 얻고 부모 디렉토리를 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import streamlit as st
from IntegrationChat import chatbot_response, questions, retrieve_depression_state

# Streamlit 설정
st.set_page_config(layout="wide")
st.title("Mental Health")

# 두 개의 열 생성, 중간에 여백을 추가
chatbot_col, spacer, survey_col = st.columns([1, 0.1, 1])

with chatbot_col:
    st.header("🤖 Mental Health Chatbot")
    
    # CSS 스타일 정의
    st.markdown("""
        <style>
        .chatbox {
            background-color: #e6f7ff;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .user-message {
            background-color: #F1F8E8;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .bot-message {
            background-color: #fff1e6;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # 대화 이력을 저장할 리스트
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    user_input = st.text_input("How are you feeling today?:")

    if st.button("Send"):
        if user_input:
            # 사용자의 입력과 챗봇의 응답을 대화 이력에 추가
            st.session_state.conversation_history.append({"user": user_input})
            response = chatbot_response(user_input)
            st.session_state.conversation_history.append({"bot": response})

            # 감정 분석이 "negative"이면 우울증 질문 시작
            if response.startswith("Check about depression rate."):
                st.session_state.depression_responses = []
                st.session_state.current_question_index = 0

    # 대화 이력을 화면에 출력
    for chat in st.session_state.conversation_history:
        if "user" in chat:
            st.markdown(f"""
                <div class="user-message">
                    **You:** {chat['user']}
                </div>
                """, unsafe_allow_html=True)
        if "bot" in chat:
            st.markdown(f"""
                <div class="bot-message">
                    **Chatbot:** {chat['bot']}
                </div>
                """, unsafe_allow_html=True)


with survey_col:
    st.header("✏️ Check Your Depression Degree!")

    # CSS 스타일 정의
    st.markdown("""
        <style>
        .question-box {
            background-color: #FEFAE0;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    # 우울증 관련 질문 상태를 저장할 리스트
    if 'depression_responses' not in st.session_state:
        st.session_state.depression_responses = []

    # 현재 질문 인덱스를 저장할 상태
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    # 우울증 관련 질문 단계별 진행
    total_questions = len(questions)
    if st.session_state.current_question_index < total_questions:
        current_question_num = st.session_state.current_question_index + 1
        question = questions[st.session_state.current_question_index]
        st.markdown(f"""
            <div class="question-box">
                <strong>Question {current_question_num}/{total_questions}:</strong><br>{question}
            </div>
            """, unsafe_allow_html=True)
        answer = st.selectbox(
            "Select your answer (1-5):",
            ["1: Not at all", "2: A little bit", "3: Moderately", "4: Quite a bit", "5: Very much"],
            key=f"answer_{st.session_state.current_question_index}"
        )

        if st.button("Next Question", key="next_question_button"):
            st.session_state.depression_responses.append(int(answer[0]))  # 첫 번째 문자(숫자)를 정수로 변환하여 저장
            st.session_state.current_question_index += 1

            # 모든 질문이 완료되면 결과를 계산
            if st.session_state.current_question_index >= len(questions):
                depression_state = retrieve_depression_state(st.session_state.depression_responses)
                st.markdown(f"**Depression Rate:** {depression_state}")
    else:
        st.markdown("Complete Self-check. Keep talking with chatBot!")
