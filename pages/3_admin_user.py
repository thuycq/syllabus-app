import streamlit as st
import json
import os
from utils import setup_page

# Cấu hình page
setup_page("Syllabus App - Admin Quản lý tài khoản", "📚")

USER_FILE = "users.json"

# Load users
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save users
def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Load dữ liệu người dùng
users = load_users()

st.set_page_config(page_title="Quản lý tài khoản", layout="centered")
st.title("👥 Quản lý tài khoản")

# ======= Hiển thị danh sách tài khoản =======
st.subheader("📋 Danh sách tài khoản")

if users:
    emails_to_delete = []
    for i, (email, info) in enumerate(users.items()):
        col1, col2, col3 = st.columns([5, 4, 1])
        with col1:
            st.write(email)
        with col2:
            st.write(f"🔑 {info.get('password', '')}")
        with col3:
            if st.button("🗑️", key=f"delete_{i}"):
                emails_to_delete.append(email)

    if emails_to_delete:
        for email in emails_to_delete:
            del users[email]
        save_users(users)
        st.success(f"🗑️ Đã xóa {len(emails_to_delete)} tài khoản.")
        st.rerun()
else:
    st.info("Chưa có tài khoản nào.")

st.divider()

# ======= Thêm nhiều tài khoản cùng lúc =======
st.subheader("➕ Cấp quyền tài khoản mới")

# Biến session để lưu bảng nhập động
if "new_users" not in st.session_state:
    st.session_state.new_users = [{"email": "@uel.edu.vn", "password": "123456"}]

def add_row():
    st.session_state.new_users.append({"email": "@uel.edu.vn", "password": "123456"})

def remove_row(index):
    st.session_state.new_users.pop(index)

# Hiển thị bảng nhập email + password
for i, row in enumerate(st.session_state.new_users):
    col1, col2, col3 = st.columns([5, 4, 1])
    with col1:
        row["email"] = st.text_input("Email", value=row["email"], key=f"email_{i}", placeholder="gv01@uel.edu.vn")
    with col2:
        row["password"] = st.text_input("Mật khẩu", value=row["password"], key=f"pass_{i}", type="password")
    with col3:
        if st.button("❌", key=f"remove_{i}"):
            remove_row(i)
            st.rerun()

# Nút thêm dòng mới
st.button("➕ Thêm dòng", on_click=add_row)

# Nút xác nhận thêm tài khoản
if st.button("✅ Thêm tất cả tài khoản"):
    added = 0
    for row in st.session_state.new_users:
        email = row["email"].strip().lower()
        password = row["password"].strip()
        if (
            email.endswith("@uel.edu.vn")
            and len(password) >= 4
            and email not in users
        ):
            users[email] = {"role": "gv", "password": password}
            added += 1

    if added > 0:
        save_users(users)
        st.success(f"✅ Đã thêm {added} tài khoản.")
        st.session_state.new_users = [{"email": "", "password": ""}]
        st.rerun()
    else:
        st.warning("⚠️ Không có tài khoản nào được thêm (trùng hoặc không hợp lệ).")
