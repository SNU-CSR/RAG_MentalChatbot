# IntegrationChat.py

import sys
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 현재 파일의 디렉토리 경로를 얻고 부모 디렉토리를 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import openai
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
from Model.SentimentModel import predict_sentiment  # 감정 분석 모델 임포트
from Model.DepressionSearch import retrieve_depression_info  # 우울증 정보 검색 함수 임포트

# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')


llm = OpenAI(temperature=0.7)

# 기본적인 프롬프트 템플릿 설정
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="You are a helpful assistant. Respond to the following: {user_input}"
)

llm_chain = LLMChain(llm=llm, prompt=prompt)
chatbot_chain = SimpleSequentialChain(chains=[llm_chain])

def generate_response_gpt3(user_input):
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )
    return response.choices[0].text.strip()

def chatbot_response(user_input):
    # 감정 분석 수행
    sentiment = predict_sentiment(user_input)
    if sentiment == 'negative':
        depression_response = "우울증 위험을 평가하기 위해 몇 가지 질문에 답해주세요."
        return depression_response
    
    # 우울증 관련 질문에 답하기
    if "우울증" in user_input or "질환" in user_input:
        # 실제 구현에서는 사용자의 응답을 받아서 리스트 생성
        user_responses = [1, 2, 3, 4, 5, 2, 3, 4, 1, 2, 3, 4, 5, 2]
        depression_state = retrieve_depression_info(user_responses)
        return f"우울증 상태: {depression_state}"
    
    # 그렇지 않으면 대화 응답 생성 (LangChain 사용)
    response = chatbot_chain.run({"user_input": user_input})
    return response

# 대화 예제
if __name__ == "__main__":
    print(chatbot_response("우울증이란 무엇인가요?"))
    print(chatbot_response("오늘 너무 우울해요."))
