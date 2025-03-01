from googleapiclient.discovery import build
from auth import get_credentials
import datetime
import os

TOKEN_PATH = "token.pickle"

def authenticate_gmail():
    """저장된 OAuth 토큰을 사용하여 Gmail API 인증"""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = get_credentials()

    if not creds or not creds.valid:
        print("❌ 인증 오류! 먼저 OAuth 인증을 완료하세요.")
        return None
    
    return build("gmail", "v1", credentials=creds)

def build_query(before_days=365, from_email=None, keyword=None, exclude_from_email=None, exclude_keyword=None, exclude_important=True):
    """사용자가 설정한 조건을 기반으로 Gmail 검색 쿼리 생성"""
    conditions = []

    # 1년 이상 지난 메일 검색
    if before_days:
        date_filter = (datetime.datetime.now() - datetime.timedelta(days=before_days)).strftime("%Y/%m/%d")
        conditions.append(f"before:{date_filter}")

    # 특정 발신자 필터 (포함)
    if from_email:
        conditions.append(f"from:{from_email}")

    # 특정 키워드 포함
    if keyword:
        conditions.append(keyword)

    # 특정 발신자 제외
    if exclude_from_email:
        conditions.append(f"-from:{exclude_from_email}")

    # 특정 키워드 제외
    if exclude_keyword:
        conditions.append(f"-{exclude_keyword}")

    # 중요하지 않은 메일만 (선택적)
    if exclude_important:
        conditions.append("-is:important")

    return " ".join(conditions)

def list_emails(query):
    """ 특정 조건(query)에 맞는 이메일 목록 조회 """
    service = authenticate_gmail()
    if not service:
        return []
    
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])

    return messages

def get_email_details(message_id):
    """ 이메일의 상세 정보 가져오기 (제목, 발신자) """
    service = authenticate_gmail()
    if not service:
        return "(제목 없음)", "(발신자 없음)"
    
    msg_data = service.users().messages().get(userId="me", id=message_id).execute()
    headers = msg_data["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(제목 없음)")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "(발신자 없음)")
    
    return subject, sender

def list_old_emails(preview=True, before_days=365, from_email=None, keyword=None, exclude_from_email=None, exclude_keyword=None, exclude_important=None):
    """ 특정 조건을 포함한 오래된 이메일 목록 조회 (미리보기 포함) """
    query = build_query(before_days=before_days, from_email=from_email, keyword=keyword, exclude_from_email=exclude_from_email, exclude_keyword=exclude_keyword, exclude_important=exclude_important)
    
    messages = list_emails(query)

    if not messages:
        print("📭 삭제할 오래된 메일이 없습니다.")
        return []

    print(f"🔍 {len(messages)}개의 오래된 이메일을 찾았습니다.")

    if preview:
        print("\n📩 미리보기 (최대 10개)")
        for msg in messages[:10]:  # 최대 10개 미리보기
            subject, sender = get_email_details(msg["id"])
            print(f"📩 {sender} - {subject}")

    return messages

def list_all_old_emails(from_email=None, keyword=None):
    """ 1년 이상 지난 특정 조건의 모든 이메일을 가져옴 """
    query = build_query(from_email=from_email, keyword=keyword)

    service = authenticate_gmail()
    if not service:
        return []

    messages = []
    next_page_token = None

    while True:
        results = service.users().messages().list(userId="me", q=query, pageToken=next_page_token).execute()
        messages.extend(results.get("messages", []))
        
        next_page_token = results.get("nextPageToken", None)
        if not next_page_token:
            break  # 더 이상 가져올 메일이 없음

    print(f"📩 총 {len(messages)}개의 오래된 메일을 찾았습니다.")
    return messages
