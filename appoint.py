import streamlit as st
import pandas as pd
from datetime import datetime

# 앱 타이틀
st.title("학생 상담 기록 대시보드")

# 학생 정보 입력
st.sidebar.header("학생 상담 정보 입력")
student_id = st.sidebar.text_input("학번")
student_name = st.sidebar.text_input("이름")
consultation_content = st.sidebar.text_area("상담 내용")
consultation_date = st.sidebar.date_input("상담 날짜", datetime.today())
consultation_time = st.sidebar.time_input("상담 시간", datetime.now().time())

# 데이터 저장을 위한 빈 데이터프레임 생성
if 'consultation_data' not in st.session_state:
    st.session_state.consultation_data = pd.DataFrame(columns=["학번", "이름", "상담 내용", "날짜", "시간"])

# 상담 기록 추가 버튼
if st.sidebar.button("상담 기록 추가"):
    # 입력 데이터를 데이터프레임에 추가
    new_data = {"학번": student_id, "이름": student_name, "상담 내용": consultation_content, 
                "날짜": consultation_date, "시간": consultation_time}
    st.session_state.consultation_data = st.session_state.consultation_data.append(new_data, ignore_index=True)
    st.sidebar.success("상담 기록이 추가되었습니다!")

# 상담 기록 대시보드
st.subheader("상담 기록")
st.dataframe(st.session_state.consultation_data)
