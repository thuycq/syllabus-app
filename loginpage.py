import streamlit as st
from utils import setup_page

setup_page("Syllabus App - Đăng nhập", "📚")

# Cấu hình giao diện chính
st.set_page_config(
    page_title="Syllabus App - Đăng nhập",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"  # Ẩn sidebar mặc định
)

st.title("🔐 Đăng nhập hệ thống")

login_type = st.radio("Chọn vai trò", ["Admin", "Giảng viên"], horizontal=True)

if login_type == "Admin":
    if st.button("Đăng nhập với tài khoản Admin"):
        st.switch_page("pages/1_admin_login.py")  # KHÔNG có "pages/" ở đây
elif login_type == "Giảng viên":
    if st.button("Đăng nhập với Email UEL"):
        st.switch_page("pages/1_gv_login.py")

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
