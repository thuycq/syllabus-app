import streamlit as st
import pandas as pd
import os
from utils import setup_page
from utils_drive import download_syllabus_list_from_drive


setup_page("Syllabus App - GV", "📚")


# Thanh công cụ trên cùng: Đổi mật khẩu | Đăng xuất
col_user_empty, col_user_pass, col_user_logout = st.columns([7, 1.5, 1.5])

with col_user_pass:
    if st.button("🔐 Đổi mật khẩu"):
        st.switch_page("pages/3_gv_password.py")

with col_user_logout:
    if st.button("🚪 Đăng xuất"):
        st.switch_page("pages/1_gv_login.py")

st.title("🎓 Chuyên trang quản lý Đề cương CTĐT")

# ========== CHỌN CHƯƠNG TRÌNH ĐÀO TẠO ==========
st.subheader("📘 Chọn Chương trình đào tạo")

he = st.selectbox("Hệ đào tạo", ["(chọn option)", "Thạc sĩ", "Đại học"])
khoa = st.selectbox("Khóa học", ["(chọn option)", "23", "25"])

ctdt_options = []
ctdt_placeholder = "(chọn option)"

# Cấu hình CTĐT
if he == "Thạc sĩ":
     ctdt_options = [
        ctdt_placeholder,
        "Chuyên ngành Tài chính - Ngân hàng định hướng Nghiên cứu",
        "Chuyên ngành Tài chính - Ngân hàng định hướng Ứng dụng",
        "Chuyên ngành Công nghệ tài chính định hướng Nghiên cứu",
        "Chuyên ngành Công nghệ tài chính định hướng Ứng dụng"
        ]
elif he == "Đại học":
     if khoa == "23":
         ctdt_options = [
             ctdt_placeholder,
             "Tài chính - Ngân hàng",
             "Tài chính - Ngân hàng Tiếng Anh",
             "Công nghệ tài chính"
         ]
     elif khoa == "25":
         ctdt_options = [
             ctdt_placeholder,
             "Tài chính - Ngân hàng",
             "Tài chính - Ngân hàng Tiếng Anh",
             "Công nghệ tài chính",
             "Công nghệ tài chính liên kết doanh nghiệp"
         ]

ctdt = st.selectbox("Chương trình đào tạo", ctdt_options if ctdt_options else [ctdt_placeholder])
day_du = all([he != "(chọn option)", khoa != "(chọn option)", ctdt != "(chọn option)"])

syllabus_folder = "syllabus"

# Hàng nút chức năng
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    #if st.button("📋 Xuất danh sách môn học"):
        show_subjects = True

with col_btn2:
    if st.button("📝 Soạn mới đề cương"):
        st.switch_page("pages/4_gv_Syllabus_Create.py")

with col_btn3:
    folder_syllabus_link = "https://drive.google.com/drive/folders/1vtziPO7_zj7-JJlnxOqP568NV_nP1sK7"

    if st.button("📂 Folder đề cương"):
        # Hiện link ngay sau khi bấm
        st.markdown(
            f'<a href="{folder_syllabus_link}" target="_blank">Link Folder đề cương</a>',
            unsafe_allow_html=True
        )
        

# ========== XUẤT DANH SÁCH MÔN HỌC ==========
if day_du:
    st.markdown("### 📋 Xuất danh sách môn học")

    file_name_drive = f"Import_{he.replace(' ', '_')}_{khoa}_{ctdt.replace(' ', '_')}.xlsx"

    try:
        df = download_syllabus_list_from_drive(file_name_drive)

        st.success(f"✅ Danh sách đề cương Hệ {he} CTĐT {ctdt} Khóa {khoa}:")

        # Header
        header = st.columns([0.5, 1.5, 4, 1, 3, 1.5, 1.5])
        header[0].markdown("**STT**")
        header[1].markdown("**Mã HP**")
        header[2].markdown("**Tên HP**")
        header[3].markdown("**Số TC**")
        header[4].markdown("**Phân công**")
        header[5].markdown("**Tình trạng**")
        header[6].markdown("**Quản lý đề cương**")

        for i, row in df.iterrows():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 1.5, 4, 1, 3, 1.5, 1.5])
            ma_hp = row["Mã HP"]
            ten_hp = row["Tên HP"]
            clean_ten_hp = ten_hp.strip()

            # TẠM THỜI CHỖ CHECK FILE Syllabus (chút nữa mình sẽ hướng dẫn đồng bộ qua check Drive luôn)
            file_name_syllabus = f"{ma_hp}_ĐCCT_{clean_ten_hp}_{khoa}.docx"

            # TODO: Sau sẽ thay chỗ này bằng check_file_in_drive
            file_exists = False  # tạm thời để False, chút mình sẽ thêm check

            col1.write(row["STT"])
            col2.write(ma_hp)
            col3.write(ten_hp)
            col4.write(row["Số TC"])
            if "Tên GV soạn" in df.columns:
                col5.write(row["Tên GV soạn"])
            else:
                col5.write("")
            col6.markdown("✅ Đã có" if file_exists else "❌ Chưa có")

            # Tải về
            if file_exists:
                # sau này sẽ thêm nút tải từ Drive
                col7.write("📥 Tải về (Drive)")
            else:
                if col7.button("📝 Thêm", key=f"create_{i}"):
                    st.switch_page("pages/4_gv_Syllabus_Create.py")

    except Exception as e:
        st.warning(f"⚠️ Chưa có danh sách đề cương cho CTĐT này. Lỗi: {e}")
else:
    st.warning("⚠️ Vui lòng chọn đầy đủ Hệ, Khóa, và Chương trình đào tạo.")
