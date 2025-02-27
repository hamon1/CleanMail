import argparse
from manage_emails import delete_old_emails, archive_email, move_email

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gmail 관리 스크립트")

    # 🗑 오래된 이메일 삭제 옵션
    parser.add_argument("--delete-old", action="store_true", help="오래된 이메일 삭제")
    parser.add_argument("--confirm", action="store_true", help="모든 오래된 이메일 삭제 실행")
    
    # 특정 조건 추가 (포함/제외)
    parser.add_argument("--from-email", type=str, help="특정 이메일에서 온 메일만 삭제")
    parser.add_argument("--keyword", type=str, help="특정 키워드를 포함한 메일만 삭제")
    parser.add_argument("--exclude-from-email", type=str, help="특정 이메일에서 온 메일 제외")
    parser.add_argument("--exclude-keyword", type=str, help="특정 키워드를 포함한 메일 제외")
    parser.add_argument("--exclude-important", action="store_true", help="중요한 메일 제외")

    # 📂 이메일 보관/이동 옵션
    parser.add_argument("--archive", type=str, help="특정 이메일 보관 (이메일 ID 필요)")
    parser.add_argument("--move", nargs=2, help="특정 이메일을 라벨로 이동 (이메일 ID, 라벨명 필요)")

    args = parser.parse_args()

    # 🗑 오래된 이메일 삭제 실행
    if args.delete_old:
        delete_old_emails(
            confirm=args.confirm,
            from_email=args.from_email,
            keyword=args.keyword,
            exclude_from_email=args.exclude_from_email,
            exclude_keyword=args.exclude_keyword,
            exclude_important=args.exclude_important
        )

    # 📂 특정 이메일 보관
    if args.archive:
        archive_email(args.archive)

    # 🏷 특정 이메일을 특정 라벨로 이동
    if args.move:
        move_email(args.move[0], args.move[1])
