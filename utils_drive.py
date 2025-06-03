import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ID của folder gốc trên Drive
ROOT_FOLDER_ID = '1vtziPO7_zj7-JJlnxOqP568NV_nP1sK7'

def create_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive']

    json_content = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if json_content:
        info = json.loads(json_content)
        creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    else:
        LOCAL_JSON_PATH = 'syllabus-app-drive-api.json'
        creds = service_account.Credentials.from_service_account_file(LOCAL_JSON_PATH, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)
    return service

def get_or_create_folder(parent_id, folder_name):
    service = create_drive_service()

    # Tìm folder có sẵn
    query = f"'{parent_id}' in parents and name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if items:
        # Nếu có rồi → trả về ID
        folder_id = items[0]['id']
    else:
        # Nếu chưa có → tạo mới
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        file = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = file.get('id')

    return folder_id
#---Lưu list lên drive---
def upload_file_to_drive(full_file_path, trinh_do, khoa_hoc, ctdt_folder):
    service = create_drive_service()

    # Tạo cây folder giống local
    trinh_do_folder = ""
    if trinh_do.lower() == "đại học":
        trinh_do_folder = "daihoc"
    elif trinh_do.lower() == "thạc sĩ":
        trinh_do_folder = "thacsi"

    # Build cây folder
    folder_id_level1 = get_or_create_folder(ROOT_FOLDER_ID, trinh_do_folder)
    folder_id_level2 = get_or_create_folder(folder_id_level1, f"khoa{khoa_hoc}")
    folder_id_level3 = get_or_create_folder(folder_id_level2, ctdt_folder.strip().lower())

    # Upload file vào đúng folder
    file_metadata = {
        'name': os.path.basename(full_file_path),
        'parents': [folder_id_level3]
    }
    media = MediaFileUpload(full_file_path, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    print(f"Uploaded file: {file.get('name')} (ID: {file.get('id')})")
    print(f"View link: {file.get('webViewLink')}")
    return file.get('webViewLink')

def upload_syllabus_list_to_drive(df_syllabus_list, file_name="syllabus_list.xlsx"):
    service = create_drive_service()

    # ID của folder Syllabus List
    ROOT_FOLDER_ID_SYLLABUS_LIST = "ID_FOLDER_SYLLABUS_LIST"

    # Tạm lưu file Excel ra file tạm (không cần lưu local app)
    temp_file = "/tmp/" + file_name  # trên Streamlit Cloud

    # Lưu DataFrame ra file tạm
    df_syllabus_list.to_excel(temp_file, index=False)

    # Upload lên Drive
    file_metadata = {
        'name': file_name,
        'parents': [195bgTXhDa8xROajb-MUYNtYzGUbk2VlY]
    }
    media = MediaFileUpload(temp_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    print(f"Uploaded Syllabus List: {file.get('name')} (ID: {file.get('id')})")
    return file.get('webViewLink')
