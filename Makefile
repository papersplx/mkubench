.PHONY: test run install clean docs dataset build-data fetch-youtube

install:
	pip install -r requirements.txt

run:
	python run_benchmark.py

run-ollama:
	python run_benchmark.py --client ollama --model llama3

run-openai:
	python run_benchmark.py --client openai --model gpt-4

run-local:
	python run_benchmark.py --client openai --model local-model --api-base http://localhost:8000/v1

test:
	python src/parser.py
	python -c "from src.evaluator import BenchmarkEvaluator; e = BenchmarkEvaluator('dataset/mkultra_benchmark.jsonl'); print(f'Loaded {len(e.dataset)} questions')"

build-data:
	python build_dataset.py

fetch-youtube:
	python fetch_yt_transcripts.py

dataset: build-data fetch-youtube

clean:
	rm -rf results/

docs:
	cat README.md
