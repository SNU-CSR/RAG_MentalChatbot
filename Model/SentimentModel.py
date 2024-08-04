# DataPreparation 모듈에서 get_sentiment_df 함수 임포트
from Data.DataPreparation import get_sentiment_df

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

# 데이터 준비
sentiment_df = get_sentiment_df()

# 결측값을 빈 문자열로 대체
sentiment_df['statement'].fillna('', inplace=True)
sentiment_df['status'].fillna('', inplace=True)

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(sentiment_df['statement'], sentiment_df['status'], test_size=0.2, random_state=42)

# 파이프라인 구축
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression())
])

# 모델 학습
pipeline.fit(X_train, y_train)

# 모델 평가
accuracy = pipeline.score(X_test, y_test)
print("감정 분석 모델 정확도:", accuracy)

# 감정 예측 함수
def predict_sentiment(text):
    return pipeline.predict([text])[0]
