import streamlit as st
import pandas as pd
import os
import io
from utils import setup_page
from utils_drive import upload_syllabus_list_to_drive, download_syllabus_list_from_drive

setup_page("Syllabus App - Admin", "📚")

# Thanh công cụ trên cùng: Đổi mật khẩu | Đăng xuất
col_admin_empty, col_admin_pass, col_admin_logout = st.columns([7, 1.5, 1.5])

with col_admin_pass:
    if st.button("🔐 Đổi mật khẩu"):
        st.switch_page("pages/4_admin_password.py")

with col_admin_logout:
    if st.button("🚪 Đăng xuất"):
        st.switch_page("loginpage.py")
st.title("📚 Admin - Dashboard")

# ========== CHỌN CHƯƠNG TRÌNH ĐÀO TẠO ==========
st.subheader("📘 Quản lý Đề cương")

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

# ========== LẤY LIST HIỆN TRỰC TIẾP ==========
if da_chon_day_du:
    st.markdown("### 📋 Lấy danh sách đề cương cho CTĐT")

    # Đồng bộ tên file ở mọi chỗ
    file_name_drive = f"Import_{he.replace(' ', '_')}_{khoa}_{ctdt.replace(' ', '_')}.xlsx"

    try:
        df_drive = download_syllabus_list_from_drive(file_name_drive)

        st.dataframe(df_drive, use_container_width=True)
        st.success("✅ Đã tải danh sách đề cương từ Drive.")

        # Bật flag để chỉnh trực tiếp
        st.session_state["edited_df_existing"] = df_drive
        st.session_state["show_table_flag"] = True

    except Exception as e:
        st.error(f"❌ Chưa có danh sách đề cương.")
        # Tắt flag nếu lỗi
        st.session_state["show_table_flag"] = False

# ========== CHỈNH TRỰC TIẾP sau khi LẤY LIST ==========
if st.session_state.get("show_table_flag", False):
    st.markdown("### ✏️ Chỉnh sửa danh sách đề cương (từ Drive)")

    st.session_state["edited_df_existing"] = st.data_editor(
        st.session_state["edited_df_existing"],
        column_config={
            "Mã HP": st.column_config.TextColumn("Mã HP"),
            "Tên HP": st.column_config.TextColumn("Tên HP"),
            "Tên GV soạn": st.column_config.TextColumn("Tên GV soạn"),
        },
        use_container_width=True
    )

    if st.button("💾 Lưu & Upload lại danh sách lên Drive"):
        # Đảm bảo dùng cùng 1 tên file
        file_name_drive = f"Import_{he.replace(' ', '_')}_{khoa}_{ctdt.replace(' ', '_')}.xlsx"

        drive_link = upload_syllabus_list_to_drive(
            st.session_state["edited_df_existing"],
            file_name=file_name_drive
        )
        st.success(f"✅ Đã cập nhật danh sách đề cương lên Google Drive: [Mở file trên Drive]({drive_link})")

# ========== FILE MẪU EXCEL ==========
st.markdown("### 📥 Tải file mẫu danh sách đề cương (.xlsx)")

df_mau = pd.DataFrame({
    "STT": [1, 2],
    "Mã HP": ["TC101", "CNTC202"],
    "Tên HP": ["Nguyên lý tài chính", "Công nghệ tài chính số"],
    "Số TC": [3, 2],
    "Tên GV soạn": ["Nguyễn Văn A", "Trần Thị B"]
})

file_name_mau = f"Danh_sach_de_cuong_mau.xlsx"

# Dùng BytesIO để lưu Excel vào RAM
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_mau.to_excel(writer, index=False)
output.seek(0)

# Hiển thị nút download
st.download_button(
    label="⬇️ Tải file mẫu (.xlsx)",
    data=output,
    file_name=file_name_mau,
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# ========== IMPORT EXCEL & UPLOAD ==========
if da_chon_day_du:
    st.markdown("### 📤 Tải lên danh sách đề cương (.xlsx)")

    uploaded_file = st.file_uploader("Chọn file để tải lên", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df_import = pd.read_excel(uploaded_file, engine='openpyxl')
            st.session_state["df_import"] = df_import  # SAVE vào session

            st.success("✅ Đã đọc thành công file Excel. Bạn có thể chỉnh trực tiếp bên dưới:")

        except Exception as e:
            st.error(f"❌ Lỗi khi đọc file Excel: {e}")

    if "df_import" in st.session_state:
        st.session_state["df_import"] = st.data_editor(
            st.session_state["df_import"],
            column_config={
                "Mã HP": st.column_config.TextColumn("Mã HP"),
                "Tên HP": st.column_config.TextColumn("Tên HP"),
                "Tên GV soạn": st.column_config.TextColumn("Tên GV soạn"),
            },
            use_container_width=True
        )

        if st.button("💾 Lưu & Upload lên Drive (từ file import)"):
            # Dùng tên file đồng bộ
            file_name_drive = f"Import_{he.replace(' ', '_')}_{khoa}_{ctdt.replace(' ', '_')}.xlsx"

            try:
                drive_link = upload_syllabus_list_to_drive(
                    st.session_state["df_import"],
                    file_name=file_name_drive
                )
                st.success(f"✅ Đã upload danh sách đề cương lên Google Drive: [Mở file trên Drive]({drive_link})")
            except Exception as e:
                st.error(f"❌ Lỗi khi upload danh sách lên Drive: {e}")

# ========== QUẢN LÝ TÀI KHOẢN ==========
st.markdown("---")
st.markdown("### 👤 Quản lý tài khoản giảng viên")
st.page_link("pages/3_admin_user.py", label="➡️ Vào trang quản lý tài khoản", icon="🧑‍🏫")
