import streamlit as st
import pandas as pd
from src.api_handler import KRAApiHandler
from src.analyzer import HorseRacingAnalyzer
import datetime

# --- 앱 설정 ---
st.set_page_config(page_title="WinRate Lab", page_icon="🏇")

# 로직 객체 생성 (캐싱 처리로 속도 향상)
API_KEY = "a2e9ffe3bb9e7bdb1dedef05a1651989d9da1d4d42564e2fc50d656dea55cfb8"
api_handler = KRAApiHandler(API_KEY)
analyzer = HorseRacingAnalyzer()

# --- 화면 UI ---
st.title("🏇 WinRate Lab")
st.subheader("AI 경마 승식 추천")

# 1. 데이터 수집 섹션
with st.expander("📅 데이터 수집 (최초 1회)", expanded=True):
    target_date = st.date_input("날짜 선택", datetime.date.today())
    date_str = target_date.strftime("%Y%m%d")
    
    if st.button("🔄 최신 출전표 가져오기", use_container_width=True):
        with st.spinner("마사회 API 접속 중..."):
            df = api_handler.fetch_entry_data(date_str)
            if df is not None:
                api_handler.save_by_race(df)
                st.success(f"{date_str} 데이터 수집 완료!")
            else:
                st.error("데이터가 없습니다. 날짜를 확인하세요.")

st.divider()

# 2. 분석 및 추천 섹션
race_no = st.selectbox("🔢 경주 번호 선택", [str(i) for i in range(1, 13)])

if st.button("🚀 AI 승식 추천 분석", type="primary", use_container_width=True):
    df = analyzer.load_and_clean_data(race_no)
    
    if df is not None and not df.empty:
        result = analyzer.calculate_scores(df)
        
        # 상위 마필 표
        st.write(f"📊 **제 {race_no}경주 예상 순위**")
        st.dataframe(result[['마번', '마명', '기수', '점수']].head(5), hide_index=True)
        
        # 승식별 추천
        recom = analyzer.get_betting_recommendations(result)
        if recom:
            st.write("💡 **AI 승식별 추천 조합**")
            for k, v in recom.items():
                st.info(f"**{k}** \n\n {v}")
    else:
        st.warning("데이터가 없습니다. 먼저 수집 버튼을 눌러주세요.")