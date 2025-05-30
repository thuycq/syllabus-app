import streamlit as st
import json
import os

USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Kiểm tra đăng nhập
if "logged_in" not in st.session_state or st.session_state.role != "gv":
    st.error("⛔ Vui lòng đăng nhập bằng tài khoản Giảng viên.")
    st.stop()

email = st.session_state.get("user_email", "")

st.set_page_config(page_title="Đổi mật khẩu", layout="centered")
st.title("🔐 Đổi mật khẩu tài khoản")

users = load_users()

if email not in users:
    st.error("❌ Không tìm thấy tài khoản trong hệ thống.")
    st.stop()

old_pw = st.text_input("Mật khẩu hiện tại", type="password")
new_pw = st.text_input("Mật khẩu mới", type="password")
confirm_pw = st.text_input("Xác nhận mật khẩu mới", type="password")

if st.button("✅ Cập nhật mật khẩu"):
    if old_pw != users[email]["password"]:
        st.error("❌ Mật khẩu hiện tại không đúng.")
    elif len(new_pw.strip()) < 6:
        st.error("❌ Mật khẩu mới phải có ít nhất 6 ký tự.")
    elif new_pw != confirm_pw:
        st.error("❌ Mật khẩu xác nhận không khớp.")
    else:
        users[email]["password"] = new_pw
        save_users(users)
        st.success("✅ Đã đổi mật khẩu thành công.")
        st.switch_page("pages/2_gv_page.py")
