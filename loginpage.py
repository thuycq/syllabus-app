import streamlit as st
from utils import setup_page

setup_page("Syllabus App - Đăng nhập", "📚")

# --- HEADER đẹp ---
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="font-size: 28px; font-weight: bold; color: #003399;">
            📚 Hệ thống Quản lý Đề cương <br> Khoa Tài chính - Ngân hàng, UEL
        </div>
        <div>
            <img src="https://www.uel.edu.vn/Resources/Images/SubDomain/uel/Icon_UEL%20round%20blue.png" width="80">
        </div>
    </div>
    <hr style="margin-top: 10px; margin-bottom: 20px;">
    """,
    unsafe_allow_html=True
)

st.title("🔐 Đăng nhập")

login_type = st.radio("Chọn vai trò", ["Admin", "Giảng viên"], horizontal=True)

# --- CSS cho button đẹp ---
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #003399;
        color: white;
        font-weight: bold;
        padding: 0.6em 1.2em;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Xử lý nút login ---
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
