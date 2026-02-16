.PHONY: build run run-web test docker-build docker-run clean

VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

build:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	PYTHONPATH=. $(PYTHON) -m src.main

run-web:
	PYTHONPATH=. $(PYTHON) -m src.api

test:
	PYTHONPATH=. $(PYTHON) -m pytest -q

docker-build:
	docker build -t person-finder:latest .

docker-run:
	docker run --rm -e OPENAI_API_KEY=$$OPENAI_API_KEY person-finder:latest

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
