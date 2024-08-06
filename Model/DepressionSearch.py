# DepressionSearch.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Model.DepressionVector import model, client

def retrieve_faq_info(query):
    query_vector = model.encode([query], normalize_embeddings=True).tolist()
    
    results = client.get_collection("mental_health_faq").query(
        query_embeddings=query_vector,
        n_results=1
    )
    
    if results['ids']:
        first_metadata = results['metadatas'][0]
        if isinstance(first_metadata, dict):
            return first_metadata.get('Answers', "질문에 대한 답변을 찾을 수 없습니다.")
        elif isinstance(first_metadata, list) and len(first_metadata) > 0:
            return first_metadata[0].get('Answers', "질문에 대한 답변을 찾을 수 없습니다.")
        else:
            return "질문에 대한 답변을 찾을 수 없습니다."
    else:
        return "질문에 대한 답변을 찾을 수 없습니다."

# 테스트
if __name__ == "__main__":
    query = "What does it mean to have a mental illness?"
    print(retrieve_faq_info(query))