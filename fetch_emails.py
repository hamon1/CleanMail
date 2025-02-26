from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from auth import get_credentials

import os

# 저장된 OAuth 토큰 로드
TOKEN_PATH = "token.pickle"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    """ 저장된 OAuth 토큰을 사용하여 Gmail API 인증 """
    creds = None
    if os.path.exists(TOKEN_PATH):
        # creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        creds = get_credentials()

    if not creds or not creds.valid:
        print("❌ 인증 오류! 먼저 OAuth 인증을 완료하세요.")
        return None
    
    return build("gmail", "v1", credentials=creds)

def fetch_emails():
    """ Gmail API를 사용하여 받은 이메일 리스트 가져오기 """
    service = authenticate_gmail()
    if not service:
        return
    
    results = service.users().messages().list(userId="me", maxResults=10).execute()
    messages = results.get("messages", [])

    if not messages:
        print("📭 새로운 이메일이 없습니다.")
        return
    
    print("📩 최근 이메일 목록:")
    for msg in messages:
        msg_id = msg["id"]
        msg_detail = service.users().messages().get(userId="me", id=msg_id).execute()
        snippet = msg_detail.get("snippet", "내용 없음")
        print(f"- {msg_id}: {snippet}")

if __name__ == "__main__":
    fetch_emails()
