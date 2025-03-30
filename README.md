
# 🏫 학교 건강 진단 챗봇 + Hugging Face GPT

이 프로젝트는 학생들이 자신의 체온과 증상을 입력해 간단한 건강 진단을 받을 수 있는 웹 챗봇입니다.  
또한 Hugging Face 무료 GPT API를 통해 건강 상담 질문 기능도 제공합니다.

## ✅ 기능
- 증상 체크박스를 통한 건강 진단
- 무료 GPT 모델(Mistral)을 이용한 건강 질문 상담
- Streamlit 기반의 웹 인터페이스

## ▶️ 실행 방법

1. 필요한 라이브러리 설치
```
pip install -r requirements.txt
```

2. 실행
```
streamlit run health_chatbot_huggingface.py
```

3. Hugging Face API 키는 [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) 에서 생성하세요.
