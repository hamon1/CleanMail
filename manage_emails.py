from googleapiclient.discovery import build
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
