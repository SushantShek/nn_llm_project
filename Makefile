.PHONY: build run test docker-build docker-run clean

build:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && python -m src/main

test:
	pytest -q

docker-build:
	docker build -t nn-assignment:latest .

docker-run:
	docker run --rm -e HF_API_KEY=$$HF_API_KEY -e HF_MODEL=$$HF_MODEL nn-assignment:latest

clean:
	rm -rf .venv
