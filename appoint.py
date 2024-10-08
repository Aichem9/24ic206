import streamlit as st
import pandas as pd
from datetime import datetime

# CSV 파일 경로
csv_file_path = "reservations.csv"

# CSV 파일에서 데이터를 불러오는 함수
def load_data():
    try:
        return pd.read_csv(csv_file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["학번", "이름", "상담 항목", "예약 날짜", "예약 시간", "코멘트"])

# 데이터를 CSV 파일에 저장하는 함수
def save_data(df):
    df.to_csv(csv_file_path, index=False)

# 앱 타이틀
st.title("학생 상담 예약 대시보드")

# CSV 파일에서 예약 데이터 불러오기
if 'reservation_data' not in st.session_state:
    st.session_state.reservation_data = load_data()

# 학생 예약 정보 입력
st.sidebar.header("상담 예약 정보 입력")
student_id = st.sidebar.text_input("학번")
student_name = st.sidebar.text_input("이름")
consultation_type = st.sidebar.selectbox("상담 항목 선택", ["내신", "수능", "진학", "기타"])
reservation_date = st.sidebar.date_input("예약 날짜", datetime.today())
reservation_time = st.sidebar.time_input("예약 시간", datetime.now().time())
comment = st.sidebar.text_area("코멘트", "상담에 대한 추가 내용을 입력하세요.")

# 상담 예약 추가 버튼
if st.sidebar.button("상담 예약 추가"):
    # 중복 확인
    existing_reservations = st.session_state.reservation_data[
        (st.session_state.reservation_data["예약 날짜"] == str(reservation_date)) &
        (st.session_state.reservation_data["예약 시간"] == str(reservation_time))
    ]
    
    if not existing_reservations.empty:
        st.sidebar.error("해당 날짜와 시간에 이미 예약이 존재합니다. 다른 시간을 선택해 주세요.")
    else:
        # 입력 데이터를 데이터프레임에 추가
        new_reservation = {
            "학번": student_id, 
            "이름": student_name, 
            "상담 항목": consultation_type, 
            "예약 날짜": str(reservation_date), 
            "예약 시간": str(reservation_time), 
            "코멘트": comment
        }

        # 새로운 데이터를 세션 상태와 CSV 파일에 저장
        st.session_state.reservation_data = pd.concat([st.session_state.reservation_data, pd.DataFrame([new_reservation])], ignore_index=True)
        save_data(st.session_state.reservation_data)  # 데이터 저장
        st.sidebar.success("상담 예약이 추가되었습니다!")

# 예약된 상담 내역 대시보드
st.subheader("예약된 상담 내역")
st.dataframe(st.session_state.reservation_data)
