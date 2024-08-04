import pandas as pd
import json

# 정신건강 FAQ 데이터셋
faq_df = pd.read_csv('Mental_Health_FAQ.csv')

print(faq_df.head())

# 정신건강 데이터셋
with open('Mental_Health_Conversations.json', 'r', encoding='utf-8') as file:
    conversation_data = json.load(file)

# patterns와 responses를 추출하여 데이터프레임으로 변환
data = []

for intent in conversation_data['intents']:
    if 'responses' in intent:
        for pattern in intent['patterns']:
            for response in intent['responses']:
                data.append({'pattern': pattern, 'response': response})
    else:
        for pattern in intent['patterns']:
            data.append({'pattern': pattern, 'response': ''})

conversation_df = pd.DataFrame(data)

# 대화 데이터 전처리
conversation_df['pattern'] = conversation_df['pattern'].str.lower()
conversation_df['response'] = conversation_df['response'].str.lower()

print(conversation_df.head())

# 감정분석 데이터 로드
sentiment_df = pd.read_csv('sentiment_analysis_data.csv')

# 결측값을 빈 문자열로 대체
sentiment_df['statement'].fillna('', inplace=True)
sentiment_df['status'].fillna('', inplace=True)

def get_sentiment_df():
    return sentiment_df

print(sentiment_df.head())

# 우울증 감지 데이터 로드
depression_df = pd.read_csv('Depression_Detection.csv')

def get_depression_df():
    return depression_df

print(depression_df.head())
