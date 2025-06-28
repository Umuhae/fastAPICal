# 🧮 FastAPI 계산기 프로젝트

이 프로젝트는 **FastAPI**, **MariaDB**, **Vanilla HTML/JS**로 구현된 로컬 웹 계산기입니다.
사용자가 입력한 수식을 서버에서 계산하고, 계산 기록을 **MariaDB**에 저장/조회/수정/삭제할 수 있습니다.

---

## 🔧 기술 스택

* **Backend**: Python 3.x, FastAPI
* **Frontend**: HTML5, JavaScript
* **Database**: MariaDB
* **환경**: macOS (Apple M1 Pro 기준, 로컬 개발 환경)

---

## 📦 주요 기능

| 기능           | 설명                                           |
| ------------ | -------------------------------------------- |
| ✅ 수식 입력 및 계산 | 사용자가 입력한 수식을 FastAPI에서 안전하게 처리 (`eval()` 기반) |
| ✅ 계산 결과 저장   | 수식과 결과를 MariaDB에 저장                          |
| ✅ 계산 기록 리스트  | 최근 계산 내역을 리스트 형태로 불러오기                       |
| ✅ 기록 재실행     | 이전 계산식을 다시 서버에 요청해 실행 가능                     |
| ✅ 기록 수정 및 삭제 | 기존 계산 내역의 수정/삭제 기능 제공                        |
| ✅ 파일 저장 (선택) | 특정 계산 결과를 로컬 파일로 저장하는 기능도 확장 가능              |

---

## 📂 프로젝트 구조

```
lifeup/
├── app/
│   ├── main.py          # FastAPI 진입점
│   ├── models.py        # SQLAlchemy 모델 정의
│   ├── crud.py          # CRUD 로직 모듈
│   └── database.py      # DB 연결 설정
├── static/
│   ├── index.html       # 계산기 UI (프론트엔드)
│   └── script.js        # 계산기 로직 (클라이언트 JS)
├── .env                 # 환경변수 (.env DB 연결정보 등)
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🚀 실행 방법

### 1. 가상환경 생성 (선택)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. MariaDB 실행 및 환경 설정

`.env` 파일 생성 후 다음 정보 포함:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=calculator_db
```

DB가 실행 중인지 확인하고, 필요한 경우 `models.py` 기준으로 테이블을 생성하세요.

### 4. FastAPI 서버 실행

```bash
uvicorn app.main:app --reload
```

### 5. 브라우저 접속

```
http://localhost:8000
```

---

## ✅ 사용 예시

* `1 + 1 * 2` 입력 → 서버에서 계산 → 결과 3 반환 → DB에 저장
* 저장된 기록 목록에서 선택 → 재계산 또는 수정/삭제 가능

---

## 🔐 보안 주의사항

현재 계산 로직은 `eval()`을 사용합니다.
**프로덕션 환경에서는 사용자 입력에 대한 철저한 검증** 또는 `safe-eval` 대체가 필요합니다.

---
