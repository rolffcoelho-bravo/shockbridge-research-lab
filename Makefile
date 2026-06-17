install:
pip install -r requirements.txt

test:
pytest

lint:
ruff check src tests examples

format:
black src tests examples

run:
python examples/run_full_pipeline.py

all: install test run
