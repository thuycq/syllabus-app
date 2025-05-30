import streamlit as st
import json
import os

st.set_page_config(page_title="Đổi mật khẩu Admin", layout="centered")
st.title("🔐 Đổi mật khẩu Admin")

# File admin_account.json
user_file = "admin_account.json"
admin_username = "admin"  # cố định

# Form đổi mật khẩu
with st.form("change_password_admin_form"):
    st.write(f"👤 Đang đăng nhập: **{admin_username}**")
    old_password = st.text_input("Mật khẩu cũ", type="password", key="admin_old_password")
    new_password = st.text_input("Mật khẩu mới", type="password", key="admin_new_password")
    confirm_password = st.text_input("Xác nhận mật khẩu mới", type="password", key="admin_confirm_password")

    submit_button = st.form_submit_button("🔐 Đổi mật khẩu")

if submit_button:
    if not os.path.exists(user_file):
        st.error("❌ Không tìm thấy file admin_account.json!")
    else:
        with open(user_file, "r", encoding="utf-8") as f:
            user_data = json.load(f)

        if user_data.get("username", "") != admin_username:
            st.error("❌ User admin không tồn tại.")
        elif user_data.get("password", "") != old_password:
            st.error("❌ Mật khẩu cũ không đúng.")
        elif new_password != confirm_password:
            st.error("❌ Mật khẩu mới không khớp.")
        else:
            user_data["password"] = new_password
            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, ensure_ascii=False, indent=4)
            st.switch_page("pages/1_admin_login.py")
