import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sklearn.metrics.pairwise import cosine_similarity
from Model.DepressionVector import model, client

def retrieve_faq_info(query, similarity_threshold=0.7):
    query_vector = model.encode([query]).tolist()
    
    results = client.get_collection("mental_health_faq").query(
        query_embeddings=query_vector,
        n_results=1
    )


    if results['ids'] and results['embeddings']:
        first_metadata = results['metadatas'][0]
        first_embedding = results['embeddings'][0]
        similarity = cosine_similarity([query_vector[0]], [first_embedding])[0][0]
        
        if similarity >= similarity_threshold:
            if isinstance(first_metadata, dict):
                return first_metadata.get('Answers', "질문에 대한 답변을 찾을 수 없습니다.")
            elif isinstance(first_metadata, list) and len(first_metadata) > 0:
                return first_metadata[0].get('Answers', "질문에 대한 답변을 찾을 수 없습니다.")
        return "질문에 대한 답변을 찾을 수 없습니다."
    else:
        return "질문에 대한 답변을 찾을 수 없습니다."

# test
if __name__ == "__main__":
    query = "Hi!"
    print(retrieve_faq_info(query))
