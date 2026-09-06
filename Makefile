.PHONY: test run install clean docs dataset build-data fetch-youtube check-env

PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) run_benchmark.py

run-ollama:
	$(PYTHON) run_benchmark.py --client ollama --model llama3

run-openai:
	$(PYTHON) run_benchmark.py --client openai --model gpt-4

run-local:
	$(PYTHON) run_benchmark.py --client openai --model local-model --api-base http://localhost:8000/v1

test:
	$(PYTHON) src/parser.py
	$(PYTHON) -m unittest discover tests/ -v

build-data:
	$(PYTHON) build_dataset.py

fetch-youtube:
	$(PYTHON) fetch_yt_transcripts.py

dataset: build-data fetch-youtube

check-env:
	$(PYTHON) -c "import requests, yaml, PyPDF2, pdfplumber, ebooklib, bs4; print('All dependencies OK')"

clean:
	rm -rf results/

docs:
	cat README.md
