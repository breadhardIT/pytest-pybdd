include .env
export
export PYTHONPATH=$(PWD)/src

PHONY: run/local
run/local:
	uv run uvicorn app.main:app --reload

PHONY: test/all
test/all:
	uv run pytest -v --html=report.html --cov=app --cov-report=html --cov-report=term-missing -o log_cli=true -o log_cli_level=INFO