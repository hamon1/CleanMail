import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# 사용할 Gmail API 권한 (메일 읽기, 삭제, 이동)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_credentials():
    creds = None
    token_path = 'token.pickle'

    # 기존 토큰 파일이 있으면 로드
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # 유효한 토큰이 없으면 다시 로그인 (OAuth 인증)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # 토큰 갱신
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)  # 로컬에서 인증 수행

        # 새 토큰 저장
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

if __name__ == "__main__":
    get_credentials()
    print("✅ OAuth 인증 완료! token.pickle 파일이 생성되었습니다.")
