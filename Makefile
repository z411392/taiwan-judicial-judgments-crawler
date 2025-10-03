include .env
export

.PHONY: \
	format \
	lint \
	demo \
	scan

.ONE_SHELL:

format:
	@uvx ruff format .

lint:
	@uvx ruff check .

demo:
	@#uv run python src/main.py scan 民事 臺灣臺北地方法院 1950-01-01 2025-09-30 --save-text
	@uv run python src/main.py scan 民事 臺灣臺北地方法院 2025-09-01 2025-09-01 --save-text --save-json

