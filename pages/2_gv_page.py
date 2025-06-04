import streamlit as st
import pandas as pd
import os
from utils import setup_page
import streamlit.components.v1 as components

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
    if st.button("📂 Folder đề cương"):
        folder_syllabus_link = "https://drive.google.com/drive/folders/1vtziPO7_zj7-JJlnxOqP568NV_nP1sK7"
        # Dùng js mở tab mới
        js = f"window.open('{folder_syllabus_link}')"  # new tab or window
        components.html(f"<script>{js}</script>", height=0)
        

# ========== XUẤT DANH SÁCH MÔN HỌC ==========
if day_du:
        file_path = os.path.join("syllabus list", f"Import_{he}_{khoa}_{ctdt.replace(' ', '_')}.xlsx")
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, engine="openpyxl")
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

                he_folder = ""
                if he.lower() == "đại học":
                    he_folder = "daihoc"
                elif he.lower() == "thạc sĩ":
                    he_folder = "thacsi"
                elif he.lower() == "tiến sĩ":
                    he_folder = "tiensi"

                ctdt_folder = ctdt.strip().lower()
                folder_path_check = os.path.join("syllabus", he_folder, f"khoa{khoa}", ctdt_folder)

                file_name = f"{ma_hp}_ĐCCT_{clean_ten_hp}_{khoa}.docx"
                file_path_check = os.path.join(folder_path_check, file_name)

                file_exists = os.path.exists(file_path_check)

                col1.write(row["STT"])
                col2.write(ma_hp)
                col3.write(ten_hp)
                col4.write(row["Số TC"])
                if "Tên GV soạn" in df.columns:
                    col5.write(row["Tên GV soạn"])
                else:
                    col5.write("")
                col6.markdown("✅ Đã có" if file_exists else "❌ Chưa có")

                # Nút Chỉnh sửa
   #             if file_exists:
    #                if col6.button("✏️ Chỉnh sửa", key=f"edit_{i}"):
     #                   st.session_state["ma_hp_selected"] = ma_hp
    #                    st.session_state["ten_hp_selected"] = ten_hp
   #                     st.session_state["khoa_selected"] = khoa
    #                    st.session_state["trinh_do_selected"] = he
    #                    st.session_state["ctdt_selected"] = ctdt
    #                    st.switch_page("pages/4_gv_Syllabus_Create.py")
     #           else:
     #               col6.markdown("🔒")  # Khóa nút nếu đã có

                # Tải về
                if file_exists:
                    with open(file_path_check, "rb") as f:
                        col7.download_button(
                            label="📥 Tải về",
                            data=f.read(),
                            file_name=file_name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"download_{i}"
                        )
                else:
                    if col7.button("📝 Thêm", key=f"create_{i}"):
                        st.switch_page("pages/4_gv_Syllabus_Create.py")
        else:
            st.warning("⚠️ Chưa có danh sách đề cương cho CTĐT này.")
else:
    st.warning("⚠️ Vui lòng chọn đầy đủ Hệ, Khóa, và Chương trình đào tạo.")
