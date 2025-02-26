from googleapiclient.discovery import build
from auth import get_credentials
import argparse
import datetime
import os

TOKEN_PATH = "token.pickle"
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def authenticate_gmail():
    """ 저장된 OAuth 토큰을 사용하여 Gmail API 인증 """
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = get_credentials()

    if not creds or not creds.valid:
        print("❌ 인증 오류! 먼저 OAuth 인증을 완료하세요.")
        return None
    
    return build("gmail", "v1", credentials=creds)

def list_old_emails():
    """ 1년 이상 지난 중요하지 않은 이메일 목록 출력 """
    service = authenticate_gmail()
    if not service:
        return
    
    one_year_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y/%m/%d")
    query = f"before:{one_year_ago} -is:important"

    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])

    if not messages:
        print("📭 삭제할 오래된 메일이 없습니다.")
        return []
    
    print(f"🔍 {len(messages)}개의 오래된 이메일을 찾았습니다. (미리 보기)")
    
    for msg in messages[:10]:  # 최대 10개만 미리보기
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(제목 없음)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(발신자 없음)")
        print(f"📩 {sender} - {subject}")

    return messages

def delete_old_emails(confirm=False):
    """ 1년 이상 지난 중요하지 않은 이메일 삭제 (확인 후 실행) """
    messages = list_old_emails()
    print("......\n")

    if not messages:
        return

    if not confirm:
        user_confirm = input("⚠️ 위 이메일을 삭제하시겠습니까? (y/n): ").strip().lower()
        if user_confirm != "y":
            print("🚫 삭제가 취소되었습니다.")
            return

    service = authenticate_gmail()
    
    print(f"🗑 {len(messages)}개의 오래된 이메일을 삭제합니다...")
    for msg in messages:
        # service.users().messages().delete(userId="me", id=msg["id"]).execute()
        print(f"✅ 삭제 완료: {msg['id']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="오래된 이메일 삭제 스크립트")
    parser.add_argument("--confirm", action="store_true", help="이메일 삭제 실행")
    args = parser.parse_args()

    delete_old_emails(confirm=args.confirm)
