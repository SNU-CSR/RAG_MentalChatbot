import sys
import os

# 현재 파일의 디렉토리를 기준으로 Data 폴더의 경로를 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data')))

# DataPreparation 모듈에서 get_sentiment_df 함수 임포트
from DataPreparation import get_depression_df

import chromadb
#from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

depression_df = get_depression_df()

# Chroma DB 클라이언트 설정
client = chromadb.Client()

# 컬렉션 생성 또는 가져오기
collection_name = 'depression'
if collection_name not in client.list_collections():
    collection = client.create_collection(name=collection_name)
else:
    collection = client.get_collection(name=collection_name)

# Sentence Transformer 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')

# 우울증 데이터 벡터화
depression_vectors = model.encode(depression_df.iloc[:, 1:-1].astype(str).apply(' '.join, axis=1).tolist())

# 우울증 데이터를 Chroma DB에 저장
ids = [str(idx) for idx in depression_df.index]
metadata = depression_df.to_dict(orient='records')

collection.add(
    ids=ids,
    embeddings=depression_vectors,
    metadatas=metadata
)

print("우울증 데이터가 Chroma DB에 저장되었습니다.")
