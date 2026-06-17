install:
	python -m pip install -r requirements.txt

test:
	python -m pytest -q

run:
	python examples/run_full_pipeline.py

lint:
	ruff check src tests examples

format:
	black src tests examples

all: install test run
