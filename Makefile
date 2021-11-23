lint:
	isort . && flake8

test:
	pytest

export_dependencies:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --dev
