import os
import re
import streamlit as st
import pandas as pd


DATA_FOLDER = "du_lieu_excel"

@st.cache_data
def load_all_exam_data(folder_path, file_name):
	all_data = []

	file_path = os.path.join(folder_path, file_name)

	try:
		xls = pd.ExcelFile(file_path)
	except Exception as e:
		st.warning(f"Lỗi khi đọc file {file_name}: {e}")
		return []
	
	df = pd.read_excel(xls, skiprows=8)

	required_cols = ["Unnamed: 2", 'Ngữ văn', 'Toán', 'Tiếng Anh', 'GDQP-AN', 'Vật lí', 'Lịch sử', 'Địa lí', 'GDKT&PL', 'Tin học']
	if all(col in df.columns for col in required_cols):
		df = df[required_cols].copy()
		all_data.append(df)
	
	if all_data:
		return pd.concat(all_data, ignore_index=True)
	else:
		return pd.DataFrame(columns=["Họ và tên", "Lớp", "Phòng thi", "Môn"])
			

def tra_cuu(data, ho_ten):
	ho_ten = ho_ten.strip().lower()

	df = data.copy()
	df["Unnamed: 2"] = df["Unnamed: 2"].astype(str).str.strip().str.lower()
	
	ket_qua = df[(df["Unnamed: 2"] == ho_ten)]

	return ket_qua[['Ngữ văn', 'Toán', 'Tiếng Anh', 'GDQP-AN', 'Vật lí', 'Lịch sử', 'Địa lí', 'GDKT&PL', 'Tin học']] if not ket_qua.empty else None

st.title("12B2")

ten = st.text_input("Họ và tên")
if st.button("Tìm"):
	if not ten:
		st.warning("Vui lòng nhập đầy đủ họ tên.")
	else:
		files = ["10B2_HKI.xlsx", "10B2_HKII.xlsx", "10B2_CN.xlsx", "11B2_HKI.xlsx", "11B2_HKII.xlsx", "11B2_CN.xlsx"]
		for file_name in files:
			subject = file_name.replace(".xlsx", "")
			LOP, HK = subject.split("_")
			data = load_all_exam_data(DATA_FOLDER, file_name)
			result = tra_cuu(data, ten)

			st.markdown(f"<h4 style='color:#007ACC;'> {HK} {LOP}</h4>", unsafe_allow_html=True)
			if result is None or result.empty:
				st.error("Không tìm thấy.")
			else:
				st.dataframe(result)

#streamlit run main.py