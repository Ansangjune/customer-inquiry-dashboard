# AGENTS.md

이 저장소는 **Harness 플랫폼의 fastapi-service 템플릿**에서 생성된 FastAPI 백엔드입니다. Codex, Claude Code, 또는 유사한 AI 에이전트가 이 프로젝트를 작업할 때 이 가이드를 따르세요.

## 빌드/테스트/lint

```powershell
# 의존성 설치
uv sync

# 테스트 실행
uv run pytest

# lint + format
uv run ruff check .
uv run ruff format .

# 타입 체크 (권고)
uv run mypy .

# 개발 서버
uv run uvicorn customer_inquiry_dashboard.main:app --reload
```

## 디렉토리 구조 (권장 패턴)

> **현재 골격에는 main.py, settings.py만 있습니다.** 아래 표는 기능을 추가할 때 따라야 할 권장 패턴입니다. 필요한 디렉토리/파일은 직접 생성하세요.

### 항상 존재 (템플릿 골격)

| 경로 | 목적 |
|------|------|
| `src/customer_inquiry_dashboard/__init__.py` | 패키지 초기화 |
| `src/customer_inquiry_dashboard/main.py` | FastAPI 앱 팩토리 + lifespan + 라우터 등록 |
| `src/customer_inquiry_dashboard/settings.py` | pydantic-settings 환경 변수 |
| `src/customer_inquiry_dashboard/deps.py` | FastAPI Depends 헬퍼 |
| `src/customer_inquiry_dashboard/exceptions.py` | 커스텀 예외 |
| `pyproject.toml` | 의존성 + 도구 설정 |

### 기능 추가 시 직접 생성

| 패턴 | 언제 만들까 |
|---|---|
| `src/customer_inquiry_dashboard/routers/{이름}.py` | 새 API 엔드포인트 그룹 추가 시 (헬스체크 외) |
| `src/customer_inquiry_dashboard/schemas/{이름}.py` | Pydantic 응답/요청 모델 정의 시 |
| `src/customer_inquiry_dashboard/services/{이름}.py` | 비즈니스 로직, 외부 API 호출, DB 액세스 등 |
| `src/customer_inquiry_dashboard/models.py` 또는 `db/models.py` | DB 모델 (SQLAlchemy 사용 시) |
| `src/customer_inquiry_dashboard/db/__init__.py` | DB 연결, 세션 팩토리 |
| `tests/unit/test_{이름}.py` | 단위 테스트 추가 시 |
| `tests/integration/test_{이름}.py` | 통합 테스트 추가 시 |

### 핵심 원칙
- **plan에 명시된 파일은 반드시 직접 생성하세요.** "이미 있겠지" 가정 금지.
- Read 도구로 실제 파일 존재 여부를 먼저 확인.
- 새 디렉토리 생성 후 `__init__.py`도 함께 추가 (Python 패키지 인식).

## 주요 기능

이 템플릿에는 다음이 포함됩니다:

- **FastAPI 애플리케이션**: 비동기 라우트, 자동 OpenAPI 문서
- **Pydantic 모델**: 강타입 요청/응답 검증
- **환경 변수 관리**: pydantic-settings로 safe한 설정 로드
- **테스트 구조**: pytest + fixtures (mock DB, client)
- **CORS 설정**: 필요시 활성화

## PR 기대치

- **기능 + 테스트 함께**: 신규 라우트/함수는 단위 테스트 필수
- **ruff 통과**: `uv run ruff check . && uv run ruff format .`
- **HTTP 상태 코드**: 적절한 상태 코드 (200, 201, 204, 400, 404, 500)
- **에러 응답**: 일관된 schema (FastAPI HTTPException)
- **OpenAPI 문서**: Pydantic 모델로 자동 생성 (docstring 추가)
- **시크릿 금지**: 환경 변수로만 로드 (`.env` commit X)
- **의존성 감사**: `pip-audit`로 CVE 체크

## 코드 컨벤션

### 라우트 및 엔드포인트
- async def 사용 (비동기)
- 모든 경로에 HTTP 메서드 명시 (GET, POST, PUT, DELETE)
- 경로 매개변수와 쿼리 매개변수 구분

### Pydantic 모델
- 모든 요청/응답 스키마는 Pydantic 모델로 정의
- 필수/선택 필드 명확히 (Optional[T] vs T)
- 모든 모델에 docstring 포함

### 에러 처리
- HTTPException으로 클라이언트 에러 반환 (FastAPI 자동 처리)
- 예외는 적절한 status_code와 함께
- 내부 에러는 로그 (detail에 노출 금지)

### 비동기
- 모든 라우트는 async
- await 누락 주의
- 데이터베이스 쿼리는 비동기 드라이버 (예: asyncpg, async SQLAlchemy)

## 코드 리뷰 가이드

이 프로젝트의 상세 리뷰 체크리스트는 **`code_review.md`** 파일을 참조하세요. 특히 다음을 확인하세요:

- **보안**: auth 미들웨어, CORS 설정, 외부 입력 검증
- **정확성**: HTTP 상태 코드, 비동기 처리 (await 누락 여부)
- **테스트**: 신규 라우트 테스트, edge case
- **의존성**: pip-audit 통과, CVE 없음

## 개발 서버 시작

```powershell
uv sync
uv run uvicorn customer_inquiry_dashboard.main:app --reload
```

서버는 `http://localhost:8000`에서 실행되며, OpenAPI 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.

## 환경 변수

`.env` 파일 (git 제외)에 민감한 값을 설정하세요:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
```

`settings.py`에서 `pydantic_settings.BaseSettings`로 로드합니다.

## 마이그레이션/데이터베이스

이 템플릿에 DB가 포함되면 (optional):

```powershell
uv run alembic upgrade head
```

Forward-only 마이그레이션만 추가하세요.

## 질문이나 모호함

- 부모 Harness 플랫폼의 `AGENTS.md`, `code_review.md` 참조
- 기존 라우트 코드를 패턴 참조로 사용
