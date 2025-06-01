import streamlit as st
import json
import os
from utils import setup_page

setup_page("Syllabus App - GV Login", "📚")

USER_FILE = "users.json"

# Load danh sách người dùng
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Session mặc định
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

st.title("🎓 Đăng nhập dành cho Giảng viên")

email = st.text_input("Email UEL", placeholder="vd: gv01@uel.edu.vn")
password = st.text_input("Mật khẩu", type="password")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🔐 Đăng nhập"):
        users = load_users()
        if email in users:
            if users[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.role = "gv"
                st.session_state.user_email = email
                st.success("✅ Đăng nhập thành công!")
                st.switch_page("pages/2_gv_page.py")
            else:
                st.error("❌ Sai mật khẩu.")
        else:
            st.error("❌ Email không tồn tại trong hệ thống.")

with col2:
    if st.button("🔙 Trở lại"):
        st.switch_page("loginpage.py")
