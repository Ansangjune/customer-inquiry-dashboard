.PHONY: install run test lint format check docker-build docker-run

install:
	uv sync

run:
	uv run uvicorn customer_inquiry_dashboard.main:app --reload --port 8000

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

check: lint test

docker-build:
	docker build -t customer-inquiry-dashboard .

docker-run:
	docker run -p 8000:8000 customer-inquiry-dashboard
