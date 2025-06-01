import streamlit as st
import pandas as pd
import os
from utils import setup_page

setup_page("Syllabus App - Admin", "📚")

# Thanh công cụ trên cùng: Đổi mật khẩu | Đăng xuất
col_admin_empty, col_admin_pass, col_admin_logout = st.columns([7, 1.5, 1.5])

with col_admin_pass:
    if st.button("🔐 Đổi mật khẩu"):
        st.switch_page("pages/4_admin_password.py")

with col_admin_logout:
    if st.button("🚪 Đăng xuất"):
        st.switch_page("loginpage.py")
st.title("📚 Quản lý danh sách đề cương")

# ========== CHỌN CHƯƠNG TRÌNH ĐÀO TẠO ==========
st.subheader("📘 Chọn Chương trình đào tạo")

he = st.selectbox("Hệ đào tạo", ["(chọn option)", "Tiến sĩ", "Thạc sĩ", "Đại học"])
khoa = st.selectbox("Khóa học", ["(chọn option)", "21", "23", "25"])

ctdt_options = []
ctdt_placeholder = "(chọn option)"

if he == "Tiến sĩ":
    ctdt_options = [ctdt_placeholder, "Tài chính - Ngân hàng"]
elif he == "Thạc sĩ":
    if khoa == "21":
        ctdt_options = [ctdt_placeholder, "Chuyên ngành Tài chính - Ngân hàng"]
    elif khoa == "23":
        ctdt_options = [
            ctdt_placeholder,
            "Chuyên ngành Tài chính - Ngân hàng định hướng Nghiên cứu",
            "Chuyên ngành Tài chính - Ngân hàng định hướng Ứng dụng"
        ]
    elif khoa == "25":
        ctdt_options = [
            ctdt_placeholder,
            "Chuyên ngành Tài chính - Ngân hàng định hướng Nghiên cứu",
            "Chuyên ngành Tài chính - Ngân hàng định hướng Ứng dụng",
            "Chuyên ngành Công nghệ tài chính định hướng Nghiên cứu",
            "Chuyên ngành Công nghệ tài chính định hướng Ứng dụng"
        ]
elif he == "Đại học":
    if khoa == "21":
        ctdt_options = [ctdt_placeholder, "Tài chính - Ngân hàng", "Tài chính - Ngân hàng CLC",
                        "Tài chính - Ngân hàng CLC Tiếng Anh", "Công nghệ tài chính", "Công nghệ tài chính CLC"]
    elif khoa == "23":
        ctdt_options = [ctdt_placeholder, "Tài chính - Ngân hàng", "Tài chính - Ngân hàng Tiếng Anh", "Công nghệ tài chính"]
    elif khoa == "25":
        ctdt_options = [ctdt_placeholder, "Tài chính - Ngân hàng", "Tài chính - Ngân hàng Tiếng Anh",
                        "Công nghệ tài chính", "Công nghệ tài chính liên kết doanh nghiệp"]

ctdt = st.selectbox("Chương trình đào tạo", ctdt_options if ctdt_options else [ctdt_placeholder])

da_chon_day_du = all([he != "(chọn option)", khoa != "(chọn option)", ctdt != "(chọn option)"])

if not da_chon_day_du:
    st.warning("⚠️ Vui lòng chọn đầy đủ các thông tin để tiếp tục.")
else:
    st.success(f"🎯 Đang chọn: {he} - Khóa {khoa} - {ctdt}")

# ========== NÚT LẤY DANH SÁCH ĐỀ CƯƠNG ==========
if da_chon_day_du:
    if st.button("📋 Lấy list đề cương cho CTĐT"):
        file_path = os.path.join("syllabus list", f"Import_{he}_{khoa}_{ctdt.replace(' ', '_')}.xlsx")
        if os.path.exists(file_path):
            st.session_state["edited_df_existing"] = pd.read_excel(file_path, engine="openpyxl")
            st.session_state["show_table_flag"] = True
            #st.success(f"✅ Đã tải danh sách đề cương: {os.path.basename(file_path)}")
        else:
            st.warning("⚠️ Chưa có danh sách đề cương cho CTĐT này.")
            st.session_state["show_table_flag"] = False

# Hiển thị bảng nếu có flag
if st.session_state.get("show_table_flag", False):
    #st.markdown("### ✏️ Chỉnh sửa danh sách đề cương (có thể chỉnh 'Mã HP')")
    st.session_state["edited_df_existing"] = st.data_editor(
        st.session_state["edited_df_existing"],
        column_config={
            "Mã HP": st.column_config.TextColumn("Mã HP"),
            "Tên HP": st.column_config.TextColumn("Tên HP"),
            "Tên GV soạn": st.column_config.TextColumn("Tên GV soạn"),
        },
        use_container_width=True
    )

    # Nút Lưu
    if st.button("💾 Lưu"):
        file_path = os.path.join("syllabus list", f"Import_{he}_{khoa}_{ctdt.replace(' ', '_')}.xlsx")
        st.session_state["edited_df_existing"].to_excel(file_path, index=False, engine='openpyxl')
        st.success(f"✅ Đã lưu danh sách sau chỉnh sửa: {os.path.basename(file_path)}")


# ========== FILE MẪU EXCEL ==========
#st.markdown("### 📥 Tải file mẫu danh sách đề cương (.xlsx)")

df_mau = pd.DataFrame({
    "STT": [1, 2],
    "Mã HP": ["TC101", "CNTC202"],
    "Tên HP": ["Nguyên lý tài chính", "Công nghệ tài chính số"],
    "Số TC": [3, 2],
    "Tên GV soạn": ["Nguyễn Văn A", "Trần Thị B"]
})

folder_path = "syllabus list"
os.makedirs(folder_path, exist_ok=True)

file_name = f"Danh sách đề cương mẫu.xlsx"
file_path = os.path.join(folder_path, file_name)
df_mau.to_excel(file_path, index=False, engine='openpyxl')

with open(file_path, "rb") as f:
    st.download_button(
        label="⬇️ Tải file mẫu (.xlsx)",
        data=f.read(),
        file_name=file_name,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# ========== IMPORT EXCEL ==========
uploaded_file = st.file_uploader("📤 Tải lên List đề cương (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df_import = pd.read_excel(uploaded_file, engine='openpyxl')
        #st.success("✅ Đã đọc thành công file Excel.")

        # LƯU LUÔN FILE VÀO THƯ MỤC syllabus list
        save_folder = "syllabus list"
        os.makedirs(save_folder, exist_ok=True)

        save_path = os.path.join(save_folder, f"Import_{he}_{khoa}_{ctdt.replace(' ', '_')}.xlsx")
        df_import.to_excel(save_path, index=False, engine='openpyxl')

        st.success(f"✅ Đã lưu danh sách đề cương: {os.path.basename(save_path)}")

    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file Excel: {e}")


# ========== QUẢN LÝ TÀI KHOẢN ==========
st.markdown("---")
st.markdown("### 👤 Quản lý tài khoản giảng viên")
st.page_link("pages/3_admin_user.py", label="➡️ Vào trang quản lý tài khoản", icon="🧑‍🏫")
