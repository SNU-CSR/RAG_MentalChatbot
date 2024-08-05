from Model.DepressionVector import model, client

def retrieve_faq_info(query):
    query_vector = model.encode([query], normalize_embeddings=True).tolist()
    
    results = client.get_collection("mental_health_faq").query(
        query_embeddings=query_vector,
        n_results=1
    )
    
    if results['ids']:
        return results['metadatas'][0].get('Answers', "질문에 대한 답변을 찾을 수 없습니다.")
    else:
        return "질문에 대한 답변을 찾을 수 없습니다."

# 테스트
# if __name__ == "__main__":
    # query = "What does it mean to have a mental illness?"
    # print(retrieve_faq_info(query))
