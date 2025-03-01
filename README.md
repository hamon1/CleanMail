# CleanMail

# 📩 Gmail 자동 정리 프로그램

이 프로그램은 Gmail API를 사용하여 이메일을 자동으로 정리하는 Python 스크립트입니다.

- 특정 발신자나 키워드를 기준으로 이메일을 **보관/라벨 이동**
- 일정 기간이 지난 이메일을 **자동 삭제**
- **자동 실행(cron job)** 을 통해 정기적으로 이메일 정리 가능

-> ! 한 번에 100개 단위로 실행됩니다.

---

## 📌 1. 사전 준비

### 1.1 필수 조건

- Python 3.x 버전 설치
- Gmail API 사용을 위한 Google Cloud 설정 완료
- `credentials.json` (Google OAuth 인증 파일)

### 1.2 필요한 패키지 설치

아래 명령어를 실행하여 필요한 Python 패키지를 설치하세요.

```sh
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## ⚙ 2. 설정 파일(`config.json`) 작성

이메일 정리 기준을 설정하는 파일입니다.

### 2.1 `config.json` 파일 생성 및 작성 예시

```json
{
    "delete_old": {
        "enabled": true,
        "exclude_important": true
    },
    "organize": [
        {
            "from": "newsletter@example.com",
            "keyword": "할인",
            "label": "프로모션"
        },
        {
            "from": "boss@company.com",
            "keyword": "보고서",
            "label": "업무"
        }
    ]
}
```

### 2.2 설정 설명

- `delete_old.enabled`: **오래된 이메일 삭제 활성화 여부** (true/false)
- `delete_old.exclude_important`: **중요한 이메일 삭제 제외 여부**
- `organize`: **이메일 자동 정리 규칙 목록**
  - `from`: 특정 발신자의 이메일 주소
  - `keyword`: 제목/본문에 포함된 키워드
  - `label`: 이동할 Gmail 라벨 (없으면 생략 가능)

---

## 🚀 3. 실행 방법

### 3.1 수동 실행

아래 명령어를 실행하면 설정에 따라 이메일을 정리합니다.

```sh
python auto_clean.py
```

### 3.2 무한 반복 실행 (매일 자동 실행)

```sh
python auto_clean.py --loop
```

---

## ⏰ 4. 자동 실행 (크론잡 설정)

Linux/Mac 환경에서는 `cron`을 이용해 자동 실행할 수 있습니다.

### 4.1 크론잡 설정

1. 터미널에서 `crontab -e` 실행
2. 아래 내용을 추가하여 매일 오전 3시에 자동 실행되도록 설정

```sh
0 3 * * * /usr/bin/python3 /Users/사용자명/CleanMail/auto_clean.py
```

(※ `/usr/bin/python3` 경로는 본인의 환경에 맞게 수정하세요.) => python3 위치
(※ `/Users/사용자명/CleanMail/auto_clean.py` 경로는 본인의 환경에 맞게 수정하세요.) => auto_clean.py 위치

### 4.2 크론잡 정상 등록 확인

```sh
crontab -l
```

### 4.3 크론잡 실행 로그 확인

```sh
tail -f cleanmail.log
```

---

### ❓ 크론잡이 실행되지 않음

#### 🔹 확인할 사항:

- `auto_clean.py` 파일 경로가 올바른지 확인
- Python 경로 확인 (`which python3` 명령어 실행)
- `crontab -l`로 크론잡이 정상 등록되었는지 확인

--- v 0.0.1

이제 자동으로 깔끔한 메일함을 유지하세요! 🚀

