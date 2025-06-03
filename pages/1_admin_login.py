import streamlit as st
import json
import os
from utils import setup_page

setup_page("Syllabus App - Admin Login", "📚")

ADMIN_FILE = "admin_account.json"

# Load admin info
def load_admin():
    if os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"username": "admin", "password": "123456"}

# Session mặc định
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

st.title("🔐 Đăng nhập")

username = st.text_input(placeholder="Username")
password = st.text_input(placeholder="Password", type="password")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🔐 Đăng nhập"):
        admin = load_admin()
        if username == admin.get("username") and password == admin.get("password"):
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.success("✅ Đăng nhập thành công!")
            st.switch_page("pages/2_admin_page.py")
        else:
            st.error("❌ Sai tài khoản hoặc mật khẩu.")

with col2:
    if st.button("🔙 Trở lại"):
        st.switch_page("loginpage.py")
