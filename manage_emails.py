# from googleapiclient.discovery import build
from list_emails import authenticate_gmail, list_old_emails, get_email_details
from tqdm import tqdm
import os
import time

def delete_old_emails(confirm=False, from_email=None, keyword=None, exclude_from_email=None, exclude_keyword=None, exclude_important=None):
    """ 1년 이상 지난 중요하지 않은 이메일 삭제 (미리보기 제공) """
    messages = list_old_emails(preview=True, from_email=from_email, keyword=keyword, exclude_from_email=exclude_from_email, exclude_keyword=exclude_keyword, exclude_important=exclude_important)  # 삭제 전에 미리보기 제공
    # def list_old_emails(preview=True, before_days=365, from_email=None, keyword=None, exclude_from_email=None, exclude_keyword=None, exclude_important=None):

    if not messages:
        print("📭 삭제할 오래된 메일이 없습니다.")
        return

    if not confirm:
        user_confirm = input("\n⚠️ 위 이메일을 삭제하시겠습니까? (y/n): ").strip().lower()
        if user_confirm != "y":
            print("🚫 삭제가 취소되었습니다.")
            return

    """ 특정 이메일 목록을 삭제 (진행률 바 표시) """
    service = authenticate_gmail()
    if not service or not messages:
        return

    total = len(messages)
    print(f"\n🗑 {total}개의 이메일을 삭제합니다...\n")

    with tqdm(total=total, desc="삭제 진행", unit="메일") as pbar:
        for msg in messages:
            subject, sender = get_email_details(msg["id"])

            # 실제 삭제 수행 (테스트 시 주석 처리)
            # service.users().messages().delete(userId="me", id=msg["id"]).execute()

            # 휴지통 이동 코드 (30일 이후 삭제)
            service.users().messages().trash(userId="me", id=msg["id"]).execute()


            pbar.set_postfix(삭제_메일=f"{sender} - {subject}")
            pbar.update(1)

def archive_email(email_id):
    """ 특정 이메일을 보관 처리 (INBOX에서 제거) """
    service = authenticate_gmail()
    if not service:
        return

    service.users().messages().modify(
        userId="me",
        id=email_id,
        body={"removeLabelIds": ["INBOX"]}
    ).execute()
    print(f"✅ 이메일 {email_id} 보관 완료!")

def move_email(email_id, label_name):
    """ 특정 이메일을 원하는 라벨로 이동 """
    service = authenticate_gmail()
    if not service:
        return
    
    label_results = service.users().labels().list(userId="me").execute()
    labels = label_results.get("labels", [])
    
    label_id = next((label["id"] for label in labels if label["name"] == label_name), None)
    if not label_id:
        print(f"❌ 라벨 '{label_name}'을 찾을 수 없습니다.")
        return
    
    service.users().messages().modify(
        userId="me",
        id=email_id,
        body={"removeLabelIds": ["INBOX"], "addLabelIds": [label_id]}
    ).execute()
    print(f"✅ 이메일 {email_id}이(가) '{label_name}'로 이동되었습니다!")

def get_label_id(service, label_name):
    """Gmail에서 라벨 ID 가져오기 (없으면 생성)"""
    label_results = service.users().labels().list(userId="me").execute()
    labels = label_results.get("labels", [])

    # 이미 존재하는 라벨 찾기
    for label in labels:
        if label["name"].lower() == label_name.lower():
            return label["id"]

    # 라벨이 없으면 생성
    new_label = service.users().labels().create(
        userId="me",
        body={"name": label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
    ).execute()
    
    print(f"🆕 라벨 '{label_name}' 생성 완료!")
    return new_label["id"]

def organize_emails(from_email=None, keyword=None, label_name="자동 정리"):
    """특정 조건에 맞는 메일을 정리하여 라벨로 이동 (받은편지함에서 제거)"""
    service = authenticate_gmail()
    if not service:
        return

    query = []
    if from_email:
        query.append(f"from:{from_email}")
    if keyword:
        query.append(f"{keyword}")

    query_str = " ".join(query)
    
    print(f"🔍 검색 조건: {query_str}")
    results = service.users().messages().list(userId="me", q=query_str).execute()
    messages = results.get("messages", [])

    if not messages:
        print("📭 정리할 이메일이 없습니다.")
        return
    
    label_id = get_label_id(service, label_name)

    for msg in messages:
        service.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={"removeLabelIds": ["INBOX"], "addLabelIds": [label_id]}
        ).execute()
        print(f"✅ 이메일 {msg['id']} → '{label_name}' 라벨로 이동 완료!")

