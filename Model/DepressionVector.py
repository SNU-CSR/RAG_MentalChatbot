# DataPreparation 모듈에서 get_depression_df 함수 임포트
from Data.DataPreparation import get_depression_df

import chromadb
from sentence_transformers import SentenceTransformer

# Chroma DB 클라이언트 설정
client = chromadb.PersistentClient(path="./chromadb_data")  # 데이터를 로컬 파일에 저장

# Sentence Transformer 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')

# 우울증 데이터 로드 및 벡터화
depression_df = get_depression_df()
depression_vectors = model.encode(depression_df.iloc[:, 1:-1].astype(str).apply(' '.join, axis=1).tolist())

# 우울증 데이터를 Chroma DB에 저장
ids = []
metadatas = []
embeddings = []

for idx, row in depression_df.iterrows():
    ids.append(str(idx))
    metadatas.append(row.to_dict())
    embeddings.append(depression_vectors[idx])

# 데이터를 저장할 컬렉션 생성
depression_collection = client.create_collection(name="depression")

# 최대 배치 크기 설정
chunk_size = 166

embeddings = [e.tolist() for e in embeddings]

# 데이터를 배치 크기로 나누어 추가
for start_idx in range(0, len(embeddings), chunk_size):
    end_idx = start_idx + chunk_size
    
    chunk_embeddings = embeddings[start_idx:end_idx]
    chunk_ids = ids[start_idx:end_idx]
    chunk_metadatas = metadatas[start_idx:end_idx]
    
    depression_collection.add(embeddings=chunk_embeddings, ids=chunk_ids, metadatas=chunk_metadatas)

print("우울증 데이터가 Chroma DB에 저장되었습니다.")

# model과 client를 모듈로 정의
__all__ = ['model', 'client']
