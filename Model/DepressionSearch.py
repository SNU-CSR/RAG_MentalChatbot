from Model.DepressionVector import model, client

def retrieve_depression_info(responses):
    response_str = ' '.join(map(str, responses))
    query_vector = model.encode([response_str], normalize_embeddings=True).tolist()
    
    results = client.get_collection("depression").query(
        query_embeddings=query_vector,
        n_results=1
    )
    
    if results['ids']:
        best_match_idx = int(results['ids'][0])
        return results['metadatas'][0].get('Depression State', "질환 정보를 찾을 수 없습니다.")
    else:
        return "질환 정보를 찾을 수 없습니다."

# 테스트
if __name__ == "__main__":
    responses = [1, 1, 1, 5, 5, 1, 5, 5, 1, 5, 5, 5, 5, 5]
    print(retrieve_depression_info(responses))
