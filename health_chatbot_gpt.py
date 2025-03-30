
import streamlit as st
import openai

# ▶ OpenAI API 키 입력 받기 (사용자 직접 입력)
openai_api_key = st.text_input("🔑 OpenAI API 키를 입력하세요", type="password")
if openai_api_key:
    openai.api_key = openai_api_key

# ▶ 진단 데이터
disease_data = [
    {
        "질병": "감기",
        "증상": ["기침", "콧물", "두통", "목 아픔"],
        "체온조건": "36.5~37.5",
        "약품": ["없음", "생강차"],
        "행동": "따뜻한 물 마시기, 보건실에서 휴식"
    },
    {
        "질병": "독감",
        "증상": ["고열", "기침", "두통", "근육통", "오한"],
        "체온조건": "38 이상",
        "약품": ["타이레놀"],
        "행동": "조퇴, 병원 방문, 휴식, 충분한 수분 섭취"
    }
]

# ▶ 전체 증상 리스트 추출 (중복 제거)
all_symptoms = sorted(set(symptom for item in disease_data for symptom in item["증상"]))

# ▶ 진단 로직
def match_temp_condition(조건, 체온):
    if "이상" in 조건:
        기준 = float(''.join(filter(str.isdigit, 조건)))
        return 체온 >= 기준
    elif "~" in 조건:
        low, high = map(float, 조건.replace("℃", "").split("~"))
        return low <= 체온 <= high
    elif "정상" in 조건:
        return 36.0 <= 체온 <= 37.5
    elif "미열" in 조건:
        return 37.0 <= 체온 < 38.0
    elif "무관" in 조건 or "관계 없음" in 조건:
        return True
    return True

def diagnose(체온, 선택증상목록):
    for 항목 in disease_data:
        조건일치 = match_temp_condition(항목["체온조건"], 체온)
        증상일치 = any(증상 in 선택증상목록 for 증상 in 항목["증상"])
        if 조건일치 and 증상일치:
            return 항목
    return {"질병": "알 수 없음", "약품": [], "행동": "보건실에 방문하여 상담을 받으세요."}

def ask_gpt(question):
    if not openai_api_key:
        return "❗ OpenAI API 키를 입력해야 GPT 사용이 가능합니다."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 친절한 학교 건강 상담 챗봇이야."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ 오류 발생: {e}"

# ▶ Streamlit UI
st.title("🏫 학교 건강 진단 챗봇 + GPT")
st.markdown("체온과 증상을 선택하면 진단을 제공하고, GPT에게 질문도 할 수 있어요!")

체온 = st.slider("🌡️ 현재 체온을 선택하세요", 35.0, 41.0, 36.8, 0.1)
선택한_증상들 = st.multiselect("🤒 증상을 선택하세요", options=all_symptoms)

if st.button("✅ 진단하기"):
    if 선택한_증상들:
        결과 = diagnose(체온, 선택한_증상들)
        st.subheader("🔍 진단 결과")
        st.write(f"• 질병: **{결과['질병']}**")
        st.write(f"• 추천 약품: {', '.join(결과['약품']) if 결과['약품'] else '없음'}")
        st.write(f"• 추천 행동: {결과['행동']}")
    else:
        st.warning("증상을 하나 이상 선택해주세요.")

st.divider()
st.subheader("💬 GPT에게 건강 상담하기")

user_question = st.text_input("궁금한 건강 질문을 입력하세요")
if st.button("💡 GPT에게 물어보기"):
    if user_question:
        with st.spinner("GPT가 생각 중입니다..."):
            answer = ask_gpt(user_question)
            st.success("GPT의 답변:")
            st.write(answer)
