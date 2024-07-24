import sys
import os

# 현재 파일의 디렉토리를 기준으로 Data 폴더의 경로를 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data')))

# DataPreparation 모듈에서 get_sentiment_df 함수 임포트
from DataPreparation import get_depression_df

from chromadb import ChromaDBClient
from chromadb.config import ClientConfig
from sentence_transformers import SentenceTransformer

depression_df = get_depression_df

# Chroma DB 클라이언트 설정
client = ChromaDBClient(config=ClientConfig(server='http://localhost:7700'))

# Sentence Transformer 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')

# 우울증 데이터 벡터화
depression_vectors = model.encode(depression_df.iloc[:, 1:-1].astype(str).apply(' '.join, axis=1).tolist())

# 우울증 데이터를 Chroma DB에 저장
for idx, row in depression_df.iterrows():
    client.insert('depression', {
        'id': idx,
        'vector': depression_vectors[idx],
        'metadata': row.to_dict()
    })

print("우울증 데이터가 Chroma DB에 저장되었습니다.")
