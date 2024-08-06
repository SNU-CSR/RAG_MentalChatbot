<<<<<<< HEAD
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
=======
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

# Chroma DB 클라이언트 설정
client = chromadb.PersistentClient(path="./chromadb_data")  # 데이터를 로컬 파일에 저장
# client.delete_collection(name="mental_health_faq")
>>>>>>> origin/develop

# Sentence Transformer 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')

# Mental Health FAQ 데이터 로드
mental_health_faq_df = pd.read_csv('Mental_Health_FAQ.csv')

<<<<<<< HEAD
# 우울증 데이터를 Chroma DB에 저장
ids = [str(idx) for idx in depression_df.index]
metadata = depression_df.to_dict(orient='records')

collection.add(
    ids=ids,
    embeddings=depression_vectors,
    metadatas=metadata
)
=======
def get_mental_health_faq_df():
    return mental_health_faq_df
>>>>>>> origin/develop

# 데이터를 로드하고 벡터화
mental_health_faq_df = get_mental_health_faq_df()
faq_vectors = model.encode(mental_health_faq_df['Questions'].tolist())

# 데이터를 Chroma DB에 저장
ids = []
metadatas = []
embeddings = []

for idx, row in mental_health_faq_df.iterrows():
    ids.append(str(row['Question_ID']))
    metadatas.append(row.to_dict())
    embeddings.append(faq_vectors[idx])

# 데이터를 저장할 컬렉션 생성
faq_collection = client.create_collection(name="mental_health_faq")

# 최대 배치 크기 설정
chunk_size = 70

embeddings = [e.tolist() for e in embeddings]

# 데이터를 배치 크기로 나누어 추가
for start_idx in range(0, len(embeddings), chunk_size):
    print(start_idx)
    end_idx = start_idx + chunk_size
    
    chunk_embeddings = embeddings[start_idx:end_idx]
    chunk_ids = ids[start_idx:end_idx]
    chunk_metadatas = metadatas[start_idx:end_idx]
    
    faq_collection.add(embeddings=chunk_embeddings, ids=chunk_ids, metadatas=chunk_metadatas)

print("Mental Health FAQ 데이터가 Chroma DB에 저장되었습니다.")

# model과 client를 모듈로 정의
__all__ = ['model', 'client']
