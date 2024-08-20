import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chromadb_data") 
# client.delete_collection(name="mental_health_faq")

model = SentenceTransformer('all-MiniLM-L6-v2')

mental_health_faq_df = pd.read_csv('Mental_Health_FAQ.csv')

def get_mental_health_faq_df():
    return mental_health_faq_df

# 데이터를 로드하고 벡터화
mental_health_faq_df = get_mental_health_faq_df()
faq_vectors = model.encode(mental_health_faq_df['Questions'].tolist())

ids = []
metadatas = []
embeddings = []

for idx, row in mental_health_faq_df.iterrows():
    ids.append(str(row['Question_ID']))
    metadatas.append(row.to_dict())
    embeddings.append(faq_vectors[idx])

# 컬렉션이 존재하는지 확인
try:
    faq_collection = client.get_collection(name="mental_health_faq")
    print("기존 컬렉션을 불러왔습니다. ")
except chromadb.errors.CollectionNotFoundError:
    # 컬렉션이 없을 경우 새로 생성
    faq_collection = client.create_collection(name="mental_health_faq")
    print("새 컬렉션을 생성했습니다. ")

chunk_size = 70

embeddings = [e.tolist() for e in embeddings]

for start_idx in range(0, len(embeddings), chunk_size):
    print(start_idx)
    end_idx = start_idx + chunk_size
    
    chunk_embeddings = embeddings[start_idx:end_idx]
    chunk_ids = ids[start_idx:end_idx]
    chunk_metadatas = metadatas[start_idx:end_idx]
    
    faq_collection.add(embeddings=chunk_embeddings, ids=chunk_ids, metadatas=chunk_metadatas)

print("Mental Health FAQ 데이터가 Chroma DB에 저장되었습니다.")

__all__ = ['model', 'client']