import os
import sys
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import chromadb
from sentence_transformers import SentenceTransformer
from Data.DataPreparation import get_conversation_df, get_faq_df

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

conversation_vector_path = os.path.join(current_dir, "conversation_vectors.pkl")
faq_vector_path = os.path.join(current_dir, "faq_vectors.pkl")

client = chromadb.PersistentClient(path="./chromadb_data") 
client.delete_collection(name="low_depression_conversation")
client.delete_collection(name="high_depression_faq")
model = SentenceTransformer('all-MiniLM-L6-v2')

if not os.path.exists(conversation_vector_path) or not os.path.exists(faq_vector_path):
    # 정신건강 대화 데이터 로드 및 벡터화
    conversation_df = get_conversation_df()
    conversation_vectors = model.encode(conversation_df['pattern'].tolist(), 
                                        batch_size=128, 
                                        show_progress_bar=True)
    
    # 정신건강 FAQ 데이터 로드 및 벡터화
    faq_df = get_faq_df()
    faq_vectors = model.encode(faq_df['Questions'].tolist(), 
                               batch_size=128, 
                               show_progress_bar=True)

    with open(conversation_vector_path, 'wb') as f:
        pickle.dump(conversation_vectors, f)
    with open(faq_vector_path, 'wb') as f:
        pickle.dump(faq_vectors, f)
else:
    with open(conversation_vector_path, 'rb') as f:
        conversation_vectors = pickle.load(f)
    with open(faq_vector_path, 'rb') as f:
        faq_vectors = pickle.load(f)

    conversation_df = get_conversation_df()
    faq_df = get_faq_df()

low_depression_collection = client.create_collection(name="low_depression_conversation")

high_depression_collection = client.create_collection(name="high_depression_faq")

chunk_size = 100  

print("저우울증 벡터 DB 생성 중...")
for start_idx in range(0, len(conversation_vectors), chunk_size):
    end_idx = min(start_idx + chunk_size, len(conversation_vectors))
    
    chunk_vectors = conversation_vectors[start_idx:end_idx]
    chunk_metadata = conversation_df.iloc[start_idx:end_idx].to_dict('records')
    
    low_depression_collection.add(
        ids=[str(i) for i in range(start_idx, end_idx)],
        embeddings=[vector.tolist() for vector in chunk_vectors],
        metadatas=chunk_metadata
    )
    
    print(f"저우울증 데이터 {start_idx}에서 {end_idx}까지 처리 완료")

print("고우울증 벡터 DB 생성 중...")
for start_idx in range(0, len(faq_vectors), chunk_size):
    end_idx = min(start_idx + chunk_size, len(faq_vectors))
    
    chunk_vectors = faq_vectors[start_idx:end_idx]
    chunk_metadata = faq_df.iloc[start_idx:end_idx].to_dict('records')
    
    high_depression_collection.add(
        ids=[str(faq_df.iloc[i]['Question_ID']) for i in range(start_idx, end_idx)],
        embeddings=[vector.tolist() for vector in chunk_vectors],
        metadatas=chunk_metadata
    )
    
    print(f"고우울증 데이터 {start_idx}에서 {end_idx}까지 처리 완료")

print("우울증 정도에 따른 데이터가 Chroma DB에 저장되었습니다.")
