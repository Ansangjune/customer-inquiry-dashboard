# code_review.md

이 FastAPI 서비스의 코드 변경에 대한 리뷰 체크리스트입니다.

## 1. 보안 (Security) 🔐

### 인증/인가
- [ ] auth 미들웨어 — 보호된 모든 엔드포인트에 적용
- [ ] JWT/토큰 검증 — 모든 보호된 라우트에서 의존성으로 사용
- [ ] CORS 설정 — production 도메인만 허용 (`allowed_origins`)

### 외부 입력 검증
- [ ] 모든 요청 body — Pydantic 모델로 검증
- [ ] 경로/쿼리 매개변수 — 타입 명시 (str, int, etc.)
- [ ] 파일 업로드 — 파일 크기 제한, MIME 타입 체크

### 시크릿/환경변수
- [ ] API key, 토큰 — `.env` 또는 환경 변수로만 로드
- [ ] 응답에 민감 정보 노출 안 함 (password hash, token 등)
- [ ] 로그에 시크릿 출력 금지

### 의존성 보안
- [ ] Starlette ≥ 0.49.1 (CVE-2025-54121, CVE-2025-62727)
- [ ] 기타 의존성 — `pip-audit`로 CVE 체크
- [ ] 알려진 취약점 없음

---

## 2. API 설계 (API Design) 📡

### HTTP 상태 코드
- [ ] 200 OK — 성공적 요청
- [ ] 201 Created — 리소스 생성
- [ ] 204 No Content — 성공, 응답 body 없음
- [ ] 400 Bad Request — 잘못된 입력
- [ ] 401 Unauthorized — 인증 필요
- [ ] 403 Forbidden — 권한 없음
- [ ] 404 Not Found — 리소스 없음
- [ ] 500 Internal Server Error — 서버 에러

### 에러 응답
- [ ] 일관된 에러 schema (예: `{"detail": "..."}`)
- [ ] HTTPException으로 클라이언트 에러 반환
- [ ] 내부 에러는 로그, 클라이언트에는 일반 메시지만

### OpenAPI/Swagger 문서
- [ ] Pydantic 모델 정의 — OpenAPI 자동 생성
- [ ] docstring 포함 — 라우트, 모델, 필드 설명
- [ ] `/docs` (Swagger) `/redoc` (ReDoc) 문서 정확

### RESTful 설계
- [ ] 경로는 리소스, HTTP 메서드는 동작 (`GET /items`, `POST /items`)
- [ ] 복수형 리소스명 (`/items` not `/item`)
- [ ] 버전 관리 (필요시 `/v1/items`)

---

## 3. 비동기 처리 (Async) ⚡

### async/await
- [ ] 모든 라우트 — async def
- [ ] await 누락 없음 (I/O 작업에 async 드라이버 사용)
- [ ] blocking 작업 없음 (CPU-bound는 Executor 또는 별도 워커로)

### 데이터베이스
- [ ] async SQLAlchemy 또는 asyncpg (async 드라이버)
- [ ] await를 session.execute(), connection.fetch() 등에 사용
- [ ] 트랜잭션 scope 명확 (async context manager)

### 의존성 (Depends)
- [ ] 의존성 함수도 async 가능
- [ ] 순환 의존성 없음

---

## 4. 테스트 (Testing) 🧪

### 라우트 테스트
- [ ] 신규 라우트 — TestClient로 검증
- [ ] 정상 케이스 (200, 201)
- [ ] 에러 케이스 (400, 401, 404, 500)

### Health Check
- [ ] `/health` 엔드포인트 — 200 응답
- [ ] 데이터베이스 연결 확인 (선택사항)

### Mock/Fixture
- [ ] 의존성 override 가능 (Depends 테스트)
- [ ] mock DB, 외부 API 호출
- [ ] 격리된 테스트 (부작용 없음)

### 테스트 품질
- [ ] 모든 테스트 패스
- [ ] 기존 테스트 회귀 없음
- [ ] 타이밍 의존 테스트 없음 (sleep 남용 금지)

---

## 5. 코드 스타일 (Style) 🎨

### Python 스타일
- [ ] ruff check/format 통과
- [ ] import 순서 (stdlib, 3rd party, local)
- [ ] 한 줄 길이 ≤ 100

### Pydantic 모델
- [ ] 필수/선택 필드 명확 (Optional[T] vs T)
- [ ] 기본값 명시
- [ ] docstring (field description)

### 함수/변수 명명
- [ ] snake_case (함수, 변수)
- [ ] PascalCase (클래스, Pydantic 모델)
- [ ] 설명적 네이밍

### 코멘트
- [ ] WHY가 비자명할 때만
- [ ] docstring — 모든 public 함수

---

## 6. 의존성 관리 (Dependencies) 📦

### 신규 의존성
- [ ] pip-audit로 CVE 체크
- [ ] 최소 버전 명시 (예: `fastapi>=0.115.0`)
- [ ] 의존성 그래프 순환 없음

### 버전 호환
- [ ] Python 3.10+ (또는 프로젝트 최소 버전)
- [ ] FastAPI 호환성 (마이너 업그레이드 안전)

---

## 7. 성능/운영 (Performance/Ops) 📊

### 로깅
- [ ] 중요 이벤트 로깅 (요청, 에러)
- [ ] 민감 정보 로그 금지 (password, token)
- [ ] 구조화 로깅 (부모 플랫폼 규칙)

### 성능
- [ ] DB 쿼리 최적화 (N+1 회피)
- [ ] 느린 엔드포인트 — 타임아웃/캐싱 검토
- [ ] 대량 데이터 — pagination 고려

---

## 차단 (Block) vs 권고 (Approve)

### ❌ **반드시 차단할 사항**

다음은 **변경 요청**:

1. **시크릿 하드코딩** — API key, token, password
2. **auth 미들웨어 미사용** — 보호된 라우트 노출
3. **알려진 CVE** — starlette < 0.49.1 등
4. **SQL 인젝션** — 문자열 concat (async SQLAlchemy ORM 사용)
5. **Pydantic 모델 미사용** — 외부 입력 검증 필수
6. **await 누락** — async I/O 작업
7. **Plan에 명시된 파일이 누락된 채 commit** — 실행 누락 (routers/, schemas/, services/ 등)

### ✅ **권고할 사항** (approve but comment)

1. 에러 응답 개선 (더 구체적 메시지)
2. 테스트 커버리지 확대
3. 성능 최적화 아이디어 (캐싱, pagination)
4. docstring 완성도
5. 마이너 스타일 개선

---

## 빠른 체크리스트

PR 리뷰할 때 이 순서대로:

1. **파일 diff 훑기** — 시크릿, SQL 인젝션?
2. **테스트 확인** — 신규 라우트 테스트 있는지?
3. **ruff 통과** — lint 체크?
4. **HTTP 상태 코드** — 적절한가?
5. **의존성** — pip-audit 통과?
6. **비동기** — await 누락 없는지?
7. **auth** — 보호된 라우트 미들웨어 적용?

---

## 참조

- **AGENTS.md** — 프로젝트 개요, 빌드/테스트, 컨벤션
- 부모 **Harness 플랫폼 code_review.md** — 보안, 정확성, 테스트 상세 가이드
