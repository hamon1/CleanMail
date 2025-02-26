from googleapiclient.discovery import build
from auth import get_credentials

def list_messages():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # 받은 편지함에서 최근 10개 이메일 가져오기
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    if not messages:
        print("📭 메일이 없습니다.")
    else:
        print(f"📩 최근 {len(messages)}개의 메일을 가져왔습니다.")
        for msg in messages:
            print(f"메일 ID: {msg['id']}")

if __name__ == "__main__":
    list_messages()
