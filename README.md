
# LLM Evaluation Project

A Python-based project to evaluate Large Language Model (LLM) responses using keyword matching and an LLM-as-a-Judge approach.

## Features

- Runs benchmark questions against a local LLM.
- Uses Ollama with the `llama3.2:1b` model.
- Measures response time.
- Calculates keyword-based quality scores.
- Evaluates answers using an LLM judge with a score, verdict, and reason.
- Saves evaluation results to a CSV file.
- Includes a small judge-reliability test.

## Tech Stack

- Python
- Ollama
- Llama 3.2 (1B)
- CSV
- Keyword-based evaluation
- LLM-as-a-Judge

## Project Structure

```text
LLMEvaluation/
├── evaluate.py
├── test_judge.py
├── test_judge_reliability.py
├── test_gemini.py
└── results/
    └── llama_results.csv
```

## Setup

1. Install Python 3.11 or compatible Python 3.
2. Install Ollama.
3. Download the model:

```bash
ollama pull llama3.2:1b
```

4. Activate the virtual environment:

```bash
source .venv/bin/activate
```

5. Install the required Python packages if needed:

```bash
pip install requests python-dotenv
```

## Run Evaluation

```bash
python3 evaluate.py
```

The script evaluates benchmark questions and saves the results to:

`results/llama_results.csv`

## Evaluation Metrics

- **Keyword score:** Measures how many expected keywords appear in the answer.
- **Judge score:** Rates the answer from 1 to 5.
- **Judge verdict:** Classifies the answer as good, partial, or poor.
- **Response time:** Measures how long the model takes to respond.
- **Status:** Indicates whether the model request succeeded or failed.

## Judge Reliability

A small four-case sanity test produced 2 matching verdicts out of 4 (50% agreement).

This is only a small preliminary test, not a reliable estimate of general accuracy. The judge may incorrectly assess correct or incorrect answers. Therefore, keyword scores and judge verdicts should be treated as separate signals and checked against reference answers.

## Limitations

- A small local model may produce incomplete or incorrect answers.
- Keyword matching may not understand meaning or context.
- LLM-as-a-Judge can be inconsistent.
- More benchmark examples and human-reviewed answers are needed for stronger evaluation.

## Future Improvements

- Add more benchmark questions.
- Compare multiple LLM models.
- Improve semantic evaluation.
- Add human-reviewed reference answers.
- Generate evaluation summaries and comparisons.
