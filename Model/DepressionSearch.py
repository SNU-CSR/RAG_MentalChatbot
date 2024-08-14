import sys
import os
import pickle
import chromadb
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sklearn.metrics.pairwise import cosine_similarity
from Model.DepressionVector import model, client

current_dir = os.path.dirname(os.path.abspath(__file__))
conversation_vector_path = os.path.join(current_dir, "conversation_vectors.pkl")
faq_vector_path = os.path.join(current_dir, "faq_vectors.pkl")

with open(conversation_vector_path, 'rb') as f:
    conversation_vectors = pickle.load(f)
with open(faq_vector_path, 'rb') as f:
    faq_vectors = pickle.load(f)

def retrieve_info(query, depression_level, similarity_threshold=0.5):  
    query_vector = model.encode([query]).tolist()

    if depression_level in ["No depression", "Mild"]:
        collection_name = "low_depression_conversation"
        response_key = 'response'
    else:
        collection_name = "high_depression_faq"
        response_key = 'Answers'

    try:
        collection = client.get_collection(collection_name)
    except chromadb.errors.CollectionNotFoundError:
        return f"Error: Collection {collection_name} does not exist."

    results = collection.query(
        query_embeddings=query_vector,
        n_results=1
    )

    # 결과 출력 (디버깅용)
    # print(f"Query Vector: {query_vector}")
    # print(f"Results: {results}")

    if results['ids'] and results['embeddings']:
        first_metadata = results['metadatas'][0]
        first_embedding = results['embeddings'][0]
        similarity = cosine_similarity([query_vector[0]], [first_embedding])[0][0]
        print(f"Similarity: {similarity}")

        if similarity >= similarity_threshold:
            if isinstance(first_metadata, dict):
                return first_metadata.get(response_key, "질문에 대한 답변을 찾을 수 없습니다.")
            elif isinstance(first_metadata, list) and len(first_metadata) > 0:
                return first_metadata[0].get(response_key, "질문에 대한 답변을 찾을 수 없습니다.")
        return f"유사도가 낮습니다: {similarity}"
    else:
        return "질문에 대한 답변을 찾을 수 없습니다."

# test
if __name__ == "__main__":
    query = "Hi!"
    depression_level = "Mild"  
    print(retrieve_info(query, depression_level))