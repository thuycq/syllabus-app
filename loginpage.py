import streamlit as st

st.set_page_config(page_title="Chọn loại đăng nhập", layout="centered")
st.title("🔐 Đăng nhập hệ thống")

login_type = st.radio("Chọn vai trò", ["Admin", "Giảng viên"], horizontal=True)

if login_type == "Admin":
    if st.button("Đăng nhập với tài khoản Admin"):
        st.switch_page("pages/1_admin_login.py")  # KHÔNG có "pages/" ở đây
elif login_type == "Giảng viên":
    if st.button("Đăng nhập với Email UEL"):
        st.switch_page("pages/1_gv_login.py")
