lint:
	isort . && flake8

test:
	pytest

celery:
	celery -A config worker -B -l INFO

export_dependencies:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --dev
