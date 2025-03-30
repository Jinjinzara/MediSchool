
import streamlit as st
import requests

# ------------------------
# 🔑 NewsAPI 키 입력
# ------------------------
news_api_key = st.text_input("📰 NewsAPI 키를 입력하세요", type="password")

# ------------------------
# 📰 건강 뉴스 가져오기
# ------------------------
def get_health_news(api_key):
    url = f"https://newsapi.org/v2/everything?q=질병 예방 OR 감염병&language=ko&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        return []

# ------------------------
# UI 구성
# ------------------------
st.title("MediSchool - 건강 뉴스 센터")

menu = st.sidebar.selectbox("메뉴 선택", ["건강 뉴스"])

if menu == "건강 뉴스":
    st.header("📰 최신 질병 관련 뉴스")
    if news_api_key:
        news = get_health_news(news_api_key)
        if news:
            for article in news[:5]:
                st.subheader(article["title"])
                st.write(article.get("description", ""))
                st.write(f"[기사 원문 보기]({article['url']})")
                if article.get("urlToImage"):
                    st.image(article["urlToImage"])
                st.markdown("---")
        else:
            st.warning("❗ 뉴스를 불러올 수 없습니다.")
    else:
        st.info("📰 NewsAPI 키를 입력해주세요.")
