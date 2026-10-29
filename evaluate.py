
import csv
import time
from pathlib import Path
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"



QUESTIONS = [
    {
        "category": "Python",
        "question": "Write a Python function that adds three numbers.",
        "expected_keywords": ["def", "return"],
        "expected_answer": (
            "Define a function that accepts three numbers "
            "and returns their sum using a + b + c."
        ),
    },
    {
        "category": "React Native",
        "question": "Explain React Native in simple English.",
        "expected_keywords": ["JavaScript", "Android", "iOS"],
        "expected_answer": (
            "React Native is a framework for building Android "
            "and iOS mobile apps using JavaScript and React."
        ),
    },
    {
        "category": "LLM",
        "question": "Explain RAG and give one practical example.",
        "expected_keywords": [
            "retrieval-augmented generation",
            "retrieval",
            "context",
        ],
        "expected_answer": (
            "RAG means Retrieval-Augmented Generation. It retrieves "
            "relevant information from a knowledge source and gives "
            "that context to an LLM to help generate a grounded answer. "
            "For example, an ExpenseTracker chatbot can retrieve a "
            "user's expense records before answering a question."
        ),
    },
]



RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


def ask_llama(question: str) -> dict:
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": question}],
        "stream": False,
    }

    start = time.perf_counter()

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180,
        )
        elapsed = round(time.perf_counter() - start, 2)
        response.raise_for_status()

        answer = response.json()["message"]["content"]

        return {
            "model": MODEL_NAME,
            "question": question,
            "answer": answer,
            "response_time_seconds": elapsed,
            "status": "success",
            "error": "",
        }

    except (requests.RequestException, KeyError, ValueError) as error:
        elapsed = round(time.perf_counter() - start, 2)

        return {
            "model": MODEL_NAME,
            "question": question,
            "answer": "",
            "response_time_seconds": elapsed,
            "status": "failed",
            "error": f"{type(error).__name__}: {error}",
        }



def evaluate_answer(
    answer: str,
    expected_keywords: list[str],
    expected_answer: str,
) -> dict:
    answer_lower = answer.lower()

    matched_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() in answer_lower
    ]

    missing_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() not in answer_lower
    ]

    total_keywords = len(expected_keywords)
    score = (
        round(len(matched_keywords) / total_keywords * 100, 2)
        if total_keywords > 0
        else 0
    )

    return {
        "quality_score": score,
        "matched_keywords": ", ".join(matched_keywords),
        "missing_keywords": ", ".join(missing_keywords),
        "reference_answer": expected_answer,
    }

def judge_answer(question, reference_answer, model_answer):
    prompt = f"""
You are an evaluator for an LLM benchmark.

Compare the model answer with the reference answer.

Question:
{question}

Reference answer:
{reference_answer}

Model answer:
{model_answer}

Evaluate the model answer based on:
1. Correctness
2. Relevance
3. Completeness

Return only a JSON object with these fields:
- score: integer from 1 to 5
- verdict: "good", "partial", or "poor"
- reason: short explanation

Scoring guide:
5 = Correct and complete
4 = Mostly correct
3 = Partially correct
2 = Mostly incorrect
1 = Completely incorrect
Scoring guide:
5 = Fully correct, relevant, and complete
4 = Correct overall, with minor missing details
3 = Partially correct, with a significant omission
2 = Mostly incorrect, with only a small correct part
1 = Completely incorrect or unrelated

Verdict rules:
- Score 4 or 5: verdict must be "good"
- Score 3: verdict must be "partial"
- Score 1 or 2: verdict must be "poor"

The score and verdict MUST agree.
Judge factual correctness, not just wording.
Do not call a correct answer incorrect merely because
it could include more details.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=60,
        )

        response.raise_for_status()
        result = response.json()
        judgment = json.loads(result["response"])

        return judgment

    except (requests.RequestException, KeyError, ValueError) as error:
        return {
            "score": 0,
            "verdict": "error",
            "reason": str(error),
        }


def main():
    results = []
    for item in QUESTIONS:
        print(f"\nCategory: {item['category']}")
        print(f"Question: {item['question']}")
        result = ask_llama(item["question"])
        result["category"] = item["category"]

      
        if result["status"] == "success":
            quality = evaluate_answer(
                result["answer"],
                item["expected_keywords"],
                item["expected_answer"],
            )
            result.update(quality)

            judgment = judge_answer(
                item["question"],
                item["expected_answer"],
                result["answer"],
            )

            result["judge_score"] = judgment.get("score", 0)
            result["judge_verdict"] = judgment.get("verdict", "error")
            result["judge_reason"] = judgment.get("reason", "")

            print(f"Judge score: {result['judge_score']}/5")
            print(f"Judge verdict: {result['judge_verdict']}")


        else:
            result["quality_score"] = 0
            result["matched_keywords"] = ""
            result["missing_keywords"] = ", ".join(
                item["expected_keywords"]
            )
            result["judge_score"] = 0
            result["judge_verdict"] = "not_evaluated"
            result["judge_reason"] = "Model request failed"
        results.append(result)
        print(f"Status: {result['status']}")
        print(f"Response time: {result['response_time_seconds']} seconds")
        print(f"Quality score: {result['quality_score']}%")
        if result["status"] == "success":
            print(f"Answer:\n{result['answer']}")
        else:
            print(f"Error: {result['error']}")


 
    output_file = RESULTS_DIR / "llama_results.csv"

    fieldnames = [
        "category",
        "model",
        "question",
        "answer",
        "response_time_seconds",
        "status",
        "error",
        "quality_score",
        "matched_keywords",
        "missing_keywords",
        "reference_answer",
        "judge_score",
        "judge_verdict",
        "judge_reason",
    ]


    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    successful = [r for r in results if r["status"] == "success"]

    print("\n--- Evaluation Summary ---")
    print(f"Total questions: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(results) - len(successful)}")

    if successful:
        average = sum(
            r["response_time_seconds"] for r in successful
        ) / len(successful)
        print(f"Average response time: {average:.2f} seconds")

    print(f"Results saved to: {output_file}")



if __name__ == "__main__":
    main()
