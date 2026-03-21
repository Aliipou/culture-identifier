.PHONY: dev test lint install clean

install:
	pip install -r requirements.txt

dev:
	flask --app app run --debug

test:
	pytest tests/ -v --cov=analyzer --cov-report=term-missing

lint:
	ruff check . --fix

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache/ .ruff_cache/ coverage.xml
