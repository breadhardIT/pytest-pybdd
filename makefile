include .env
export
export PYTHONPATH=$(PWD)/src

PHONY: lint
lint:
	uv run ruff check . --fix
	uv run black .
	uv run mypy src

PHONY: run/local
run/local:
	docker compose up -d
	uv run uvicorn app.main:app --reload

PHONY: test/all
test/all:
	uv run pytest -v --html=report.html --cov=app --cov-report=html --cov-report=term-missing -o log_cli=true -o log_cli_level=INFO
