run:
		uv run main.py

lint:
		uv run ruff check

lint-fix:
		uv run ruff check --fix