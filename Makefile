build:
	uv build

check:
	uvx twine check dist/*

env:
	source .venv/bin/activate
