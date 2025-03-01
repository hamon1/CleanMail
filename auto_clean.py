import json
import time
import argparse
import logging
from datetime import datetime
from manage_emails import delete_old_emails, organize_emails

LOG_FILE = "cleanmail.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
CONFIG_PATH = "config.json"

def log(message):
    """로그 출력"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    logging.info(log_message)

def load_config():
    """설정 파일 로드"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        log("❌ 설정 파일을 찾을 수 없습니다! 먼저 'config.json'을 생성하세요.")
        return None

def auto_clean():
    """설정 파일을 기반으로 자동 정리 실행"""
    config = load_config()
    if not config:
        return
    
    log("📌 이메일 자동 정리 시작!")

    # 🗑 오래된 메일 자동 삭제
    if config.get("delete_old", {}).get("enabled", False):
        delete_old_emails(
            confirm=True,
            exclude_important=config["delete_old"].get("exclude_important", False)
        )
        log("✅ 오래된 이메일 삭제 완료")

    # 📂 이메일 자동 분류 및 정리
    for rule in config.get("organize", []):
        from_email = rule.get("from")
        keyword = rule.get("keyword")
        label = rule.get("label")
        # organize_emails(from_email=from_email, keyword=keyword, label_name=label)
        
        log(f"📂 이메일 정리: from={from_email}, keyword={keyword}, label={label or '라벨 없음'}")
        # label이 있을 때만 인자로 전달
        if label:
            organize_emails(from_email=from_email, keyword=keyword, label_name=label)
        else:
            organize_emails(from_email=from_email, keyword=keyword)

    log("✅ 이메일 자동 정리 완료!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="자동 이메일 정리 실행")
    parser.add_argument("--loop", action="store_true", help="무한 반복 실행 (스케줄링용)")
    
    args = parser.parse_args()
    
    if args.loop:
        while True:
            auto_clean()
            print("🔄 다음 실행을 기다리는 중...")
            time.sleep(86400)  # 24시간 대기 후 다시 실행 (하루 한 번)
    else:
        auto_clean()
