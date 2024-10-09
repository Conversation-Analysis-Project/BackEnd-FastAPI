from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
import numpy as np
from conversation_models import conversations

combined_conversations = {relation: ' '.join(conversation) for relation, conversation in conversations.items()}

translate = Okt()

combined_tokens = {relation: translate.morphs(text) for relation, text in combined_conversations.items()}
combined_for_vectorize = {relation: ' '.join(tokens) for relation, tokens in combined_tokens.items()}

# TF-IDF 벡터 생성
vectorizer = TfidfVectorizer(min_df=1)
X = vectorizer.fit_transform(list(combined_for_vectorize.values()))

# 대화 내용과 관계 유형 간의 유사도 계산
def classify_relationship(target_input):
    # 대상 문장에 대해 형태소 분석, 분석 결과를 공백으로 구분된 문자열로 변환
    target_tokens = translate.morphs(target_input)
    target_for_vectorize = ' '.join(target_tokens)
    t_vec = vectorizer.transform([target_for_vectorize])  # 대상 문장의 TF-IDF 벡터 생성

    # 각 관계 유형과 대상 문장 간의 코사인 유사도 계산
    cosine_similarities = {}
    for relation, combined_vector in combined_for_vectorize.items():
        combined_vec = vectorizer.transform([combined_vector])
        cosine_similarities[relation] = cosine_similarity(t_vec, combined_vec)[0][0]

    # 각 관계 유형과 대상 문장 간의 유클리드 거리 계산
    euclidean_distances = {}
    for relation, combined_vector in combined_for_vectorize.items():
        combined_vec = vectorizer.transform([combined_vector]).toarray()[0]
        target_vec_arr = t_vec.toarray()[0]
        euclidean_distances[relation] = euclidean(combined_vec, target_vec_arr)

    # 최종 점수 계산 (코사인 유사도는 최대화, 유클리드 거리는 최소화가 목적)
    final_scores = {}
    max_euclidean = np.max(list(euclidean_distances.values()))
    for relation in cosine_similarities.keys():
        cosine_score = cosine_similarities[relation]
        euclidean_score = euclidean_distances[relation]
        # 유클리드 거리를 최대화된 유클리드 거리로 나누어 점수화
        adjusted_euclidean_score = 1 - (euclidean_score / max_euclidean)
        final_score = (cosine_score + adjusted_euclidean_score) / 2
        final_scores[relation] = final_score

    closest_relation_final = max(final_scores, key=final_scores.get)

    return cosine_similarities, euclidean_distances, final_scores, closest_relation_final


# 대화 내용을 받아서 분석하는 함수 (FastAPI 요청에서 사용)
def analyze_conversation(conversation_text):
    cosine_similarities, euclidean_distances, final_scores, closest_relation_final = classify_relationship(conversation_text)

    return {
        "cosine_similarities": {relation: round(score, 4) for relation, score in cosine_similarities.items()},
        "euclidean_distances": {relation: round(score, 4) for relation, score in euclidean_distances.items()},
        "final_scores": {relation: round(score, 4) for relation, score in final_scores.items()},
        "closest_relation": closest_relation_final
    }
