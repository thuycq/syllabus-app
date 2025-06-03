import streamlit as st
from utils import setup_page

setup_page("Syllabus App - Đăng nhập", "📚")

# --- HEADER đẹp ---
col1, col2, col3 = st.columns([1, 8, 8])
with col2:
    st.markdown(
        """
        <div style="font-size: 28px; font-weight: bold; color: #003399;">
            📚 Hệ thống Quản lý Đề cương <br> Khoa Tài chính - Ngân hàng, UEL
        </div>
        """,
        unsafe_allow_html=True
    )
with col1:
    st.image("logo_temp.png", width=80)

#---Phần đăng nhập---
st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)
st.title("🔐 Đăng nhập")

login_type = st.radio(
    label = "",
    options = ["🛠️ Admin", "🎓Giảng viên"], 
    horizontal=True
)

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
if login_type == "🛠️ Admin":
    if st.button("Login"):
        st.switch_page("pages/1_admin_login.py")
elif login_type == "🎓Giảng viên":
    if st.button("Login"):
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
