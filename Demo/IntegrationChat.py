#IntegrationChat.py

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
from langchain_openai import OpenAI  
from langchain_core.runnables import RunnableSequence
#from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from Model.SentimentModel import predict_sentiment  
from Model.DepressionSearch import retrieve_faq_info  

# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

# OpenAI 클래스에 API 키를 직접 전달
llm = OpenAI(openai_api_key= openai.api_key, temperature=0.7)

#프롬프트 템플릿 설정
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="You are a helpful assistant. Respond to the following: {user_input}"
)

#llm_chain = LLMChain(llm=llm, prompt=prompt)
#chatbot_chain = SequentialChain(chains=[llm_chain])

# RunnableSequnce로 변경
chatbot_chain = RunnableSequence(prompt | llm)


questions = [
    "최근에 잠을 자지 못하거나 너무 많이 잔 적이 있나요?",
    "최근에 식욕이 감소하거나 증가한 적이 있나요?",
    "최근에 흥미를 잃은 적이 있나요?",
    "최근에 피로감을 느낀 적이 있나요?",
    "최근에 무가치함을 느낀 적이 있나요?",
    "최근에 집중하기 어려운 적이 있나요?",
    "최근에 신체적인 불안감을 느낀 적이 있나요?",
    "최근에 자살을 생각한 적이 있나요?",
    "최근에 수면 장애를 겪은 적이 있나요?",
    "최근에 공격적인 느낌을 받은 적이 있나요?",
    "최근에 공황 발작을 경험한 적이 있나요?",
    "최근에 절망감을 느낀 적이 있나요?",
    "최근에 안절부절 못한 적이 있나요?",
    "최근에 에너지가 부족하다고 느낀 적이 있나요?"
]

def generate_response_gpt3(user_input):
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# 우울상태 판단 로직
def retrieve_depression_state(user_responses):
    if all(response <= 2 for response in user_responses):
        return "No depression"
    elif all(3 <= response <= 4 for response in user_responses):
        return "Mild"
    elif all(5 <= response <= 6 for response in user_responses):
        return "Moderate"
    else:
        return "Severe"

def chatbot_response(user_input):
    # 감정 분석 수행
    sentiment = predict_sentiment(user_input)
    if sentiment == 'negative':
        depression_response = "우울증 위험을 평가하기 위해 몇 가지 질문에 답해주세요."
        print(depression_response)
        
        # 우울증 관련 질문에 답하기
        user_responses = []
        for question in questions:
            response = input(question + " (1-5): ")
            user_responses.append(int(response))
        depression_state = retrieve_depression_state(user_responses)
        print(f"우울증 상태: {depression_state}")
        
        return "이제 일반적인 대화를 시작할 수 있습니다. 궁금한 점을 물어보세요."

    # FAQ 관련 질문 처리
    faq_answer = retrieve_faq_info(user_input)
    if faq_answer != "질문에 대한 답변을 찾을 수 없습니다.":
        return faq_answer

    # 그렇지 않으면 대화 응답 생성 (LangChain 사용)
    response = chatbot_chain.run({"user_input": user_input})
    return response

# 대화 예제
# if __name__ == "__main__":
#     print(chatbot_response("우울증이란 무엇인가요?"))
#     print(chatbot_response("오늘 너무 우울해요."))

#     while True:
#         user_input = input("질문을 입력하세요: ")
#         if user_input.lower() in ["종료", "exit", "quit"]:
#             break
#         print(chatbot_response(user_input))

# __all__을 사용하여 모듈의 공개 인터페이스 정의
__all__ = ['chatbot_response']