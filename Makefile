build:
	uv build

check:
	uvx twine check dist/*

lint:
	uv run ruff check .

env:
	source .venv/bin/activate
