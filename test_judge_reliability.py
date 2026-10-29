
from evaluate import judge_answer

tests = [
    {
        "name": "Correct Python",
        "question": "Write a Python function that adds three numbers.",
        "reference": "Return a + b + c.",
        "answer": "def add_numbers(a, b, c): return a + b + c",
        "expected": "good",
    },
    {
        "name": "Incorrect Python",
        "question": "Write a Python function that adds three numbers.",
        "reference": "Return a + b + c.",
        "answer": "def add_numbers(a, b, c): return a * b * c",
        "expected": "poor",
    },
    {
        "name": "Correct RAG",
        "question": "Explain RAG.",
        "reference": "RAG means Retrieval-Augmented Generation. It retrieves relevant information and provides context to an LLM.",
        "answer": "RAG means Retrieval-Augmented Generation. It retrieves relevant information and gives it as context to an LLM.",
        "expected": "good",
    },
    {
        "name": "Incorrect RAG",
        "question": "Explain RAG.",
        "reference": "RAG means Retrieval-Augmented Generation.",
        "answer": "RAG means Remove, Arrange, and Group.",
        "expected": "poor",
    },
]

passed = 0

for test in tests:
    result = judge_answer(
        test["question"],
        test["reference"],
        test["answer"],
    )

    actual = result.get("verdict", "error")
    ok = actual == test["expected"]
    passed += int(ok)

    print(f"{test['name']}: expected={test['expected']}, actual={actual}, {'PASS' if ok else 'FAIL'}")

print(f"\nAgreement: {passed}/{len(tests)} ({passed / len(tests) * 100:.0f}%)")
