build:
	uv build

install:
    uv tool install dist/*.whl

check:
	uvx twine check dist/*

lint:
	uv run ruff check .

env:
	source .venv/bin/activate
