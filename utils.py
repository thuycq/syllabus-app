# utils.py

import streamlit as st
import datetime

# --- Setup Page ---
def setup_page(title, icon):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",  # Cho trang rộng đẹp
        initial_sidebar_state="collapsed"  # Ẩn sidebar mặc định
    )


# --- Format date to string (dùng khi xuất file Word) ---
def format_date(date_obj):
    if isinstance(date_obj, datetime.date):
        return date_obj.strftime("%d/%m/%Y")
    return ""

# --- Hiển thị tiêu đề có style đẹp ---
def styled_title(text, font_size="28px", color="#003399"):
    st.markdown(
        f"""
        <div style="font-size: {font_size}; font-weight: bold; color: {color}; margin-bottom: 10px;">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Divider (ngăn cách giữa các phần) ---
def divider():
    st.markdown("<hr style='border: 1px solid #ccc; margin: 15px 0;'>", unsafe_allow_html=True)

# --- Display success message (chuẩn hóa style) ---
def show_success(message):
    st.success(f"✅ {message}")

# --- Display error message (chuẩn hóa style) ---
def show_error(message):
    st.error(f"⚠️ {message}")
