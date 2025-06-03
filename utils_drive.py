import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ID của folder Drive
FOLDER_ID = '1vtziPO7_zj7-JJlnxOqP568NV_nP1sK7'

def create_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Kiểm tra có biến môi trường không
    json_content = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if json_content:
        # Nếu chạy trên Streamlit Cloud
        info = json.loads(json_content)
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=SCOPES
        )
    else:
        # Nếu chạy LOCAL → dùng file
        LOCAL_JSON_PATH = 'syllabus-app-drive-api.json'
        creds = service_account.Credentials.from_service_account_file(
            LOCAL_JSON_PATH, scopes=SCOPES
        )

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_drive(filename, filepath, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
    service = create_drive_service()

    file_metadata = {
        'name': filename,
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(filepath, mimetype=mimetype)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    print(f"Uploaded file: {file.get('name')} (ID: {file.get('id')})")
    print(f"View link: {file.get('webViewLink')}")
    return file.get('webViewLink')
