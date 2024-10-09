import os

import openai

# ChatGPT API 키
openai.api_key = os.getenv("OPENAI_API_KEY")


async def send_data_to_chatgpt(closest_relation, final_scores, conversation_text):
    prompt = f"""
    가장 가까운 관계: {closest_relation}
    최종 점수:
    - 썸: {final_scores.get('썸')}
    - 연애: {final_scores.get('연애')}
    - 친구: {final_scores.get('친구')}
    - 비즈니스: {final_scores.get('비즈니스')}

    최근 대화 내용:
    {conversation_text}

    위 데이터를 분석하여 400자 이내로 한국어로 요약 및 조언을 제공해주세요.
    조언 내용으로는 대인 관계나 관계 발전에 도움될 만한 조언을 제공해주세요.
    이름이 들어간 대화 내용을 출력해야 하는 경우 가능하다면 마스킹해서 출력해주세요.
    """

    # ChatGPT API 호출
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides insights."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700,
        temperature=0.7
    )

    return response['choices'][0]['message']['content']


def extract_latest_conversation(conversation_text, max_length=700):
    # 대화를 줄 단위로 분할
    conversation_lines = conversation_text.splitlines()

    total_length = 0
    selected_lines = []

    # 최신 50개의 줄 추출 (만약 50개보다 적으면 가능한 모든 줄을 추출)
    for line in conversation_lines[-50:]:
        line_length = len(line)

        # 총 글자 수가 700자를 넘으면 중단
        if total_length + line_length > max_length:
            break

        selected_lines.append(line)
        total_length += line_length

    # 줄들을 이어서 반환
    return "\n".join(selected_lines)
