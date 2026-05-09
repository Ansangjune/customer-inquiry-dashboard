# customer-inquiry-dashboard

> Harness 플랫폼이 생성한 FastAPI 백엔드 서비스입니다.

## 프로젝트 구조

```
src/customer_inquiry_dashboard/
├── main.py          # FastAPI 앱 팩토리, 라우트 정의
├── settings.py      # pydantic-settings 환경 변수
└── __init__.py

tests/
├── test_health.py   # 헬스 체크 엔드포인트 테스트
└── __init__.py
```

## 엔드포인트

| 메서드 | 경로 | 설명 | 응답 |
|---|---|---|---|
| GET | `/healthz` | 서비스 헬스 체크 | `{"status":"ok","service":"customer-inquiry-dashboard"}` |
| GET | `/docs` | OpenAPI Swagger UI | — |

## 설치

```bash
uv sync
```

## 로컬 개발

```bash
uv run uvicorn customer_inquiry_dashboard.main:app --reload
```

- HTTP: `http://localhost:8000`
- 헬스 체크: `http://localhost:8000/healthz`
- API 문서: `http://localhost:8000/docs`

## 테스트 + 품질 게이트

```bash
# 전체 테스트 실행
uv run pytest

# Lint + 포맷팅
uv run ruff check . && uv run ruff format .

# 타입 체크 (권고)
uv run mypy .
```

## 환경 변수

| 변수 | 기본값 | 설명 |
|---|---|---|
| `LOG_LEVEL` | `INFO` | 로그 레벨 |
| `SERVICE_NAME` | `customer-inquiry-dashboard` | 서비스 식별자 |

`.env` 파일에 정의하세요 (git에 commit되지 않음).

## Docker

```bash
docker build -t customer-inquiry-dashboard .
docker run -p 8000:8000 customer-inquiry-dashboard
```

## 코드 작성 가이드

이 저장소는 AI 에이전트(Claude Code, Codex 등)에 의해 변경될 수 있습니다.
- **에이전트 실행 규칙**: [`AGENTS.md`](AGENTS.md)
- **코드 리뷰 체크리스트**: [`code_review.md`](code_review.md)

## 라이선스

미정
