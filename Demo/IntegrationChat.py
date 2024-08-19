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
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from Model.SentimentModel import predict_sentiment  
from Model.DepressionSearch import retrieve_faq_info

openai.api_key = os.getenv('OPENAI_API_KEY')

llm = OpenAI(openai_api_key=openai.api_key, temperature=0.7)

# 대화 내역을 저장할 리스트
conversation_history = []

# 프롬프트 템플릿 설정
prompt = PromptTemplate(
    input_variables=["conversation_history", "user_input"],
    template=(
        "You are a helpful assistant specializing in depression prevention."
        " Below is the conversation history with the user. Based on this history, "
        "respond to the following query to help support mental health and "
        "provide useful information.\n\n"
        "Conversation history:\n{conversation_history}\n\n"
        "User's current query: {user_input}\n\n"
        "Your response:"
    )
)

# LLMChain 설정
llm_chain = LLMChain(llm=llm, prompt=prompt)

questions = [
    "1. 최근에 잠을 자지 못하거나 너무 많이 잔 적이 있나요?",
    "2. 최근에 식욕이 감소하거나 증가한 적이 있나요?",
    "3. 최근에 흥미를 잃은 적이 있나요?",
    "4. 최근에 피로감을 느낀 적이 있나요?",
    "5. 최근에 무가치함을 느낀 적이 있나요?",
    "6. 최근에 집중하기 어려운 적이 있나요?",
    "7. 최근에 신체적인 불안감을 느낀 적이 있나요?",
    "8. 최근에 자살을 생각한 적이 있나요?",
    "9. 최근에 수면 장애를 겪은 적이 있나요?",
    "10. 최근에 공격적인 느낌을 받은 적이 있나요?",
    "11. 최근에 공황 발작을 경험한 적이 있나요?",
    "12. 최근에 절망감을 느낀 적이 있나요?",
    "13. 최근에 안절부절 못한 적이 있나요?",
    "14. 최근에 에너지가 부족하다고 느낀 적이 있나요?"
]

def generate_response_gpt3(user_input):
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )
    return response.choices[0].text.strip()

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
        return "Check about depression rate."

    # 대화 내역에 사용자 입력 추가
    conversation_history.append(f"User: {user_input}")

    # FAQ 관련 질문 처리
    faq_answer = retrieve_faq_info(user_input)
    if faq_answer != "질문에 대한 답변을 찾을 수 없습니다.":
        # FAQ에서 답변을 찾은 경우, 해당 답변을 대화 내역에 추가
        conversation_history.append(f"Assistant: {faq_answer}")
        return faq_answer
    else:
        # 누적된 대화 내역을 사용하여 프롬프트 생성
        history_text = "\n".join(conversation_history)
        response = llm_chain.run({"conversation_history": history_text, "user_input": user_input})
        conversation_history.append(f"Assistant: {response}")
        return response
    
__all__ = ['chatbot_response']
