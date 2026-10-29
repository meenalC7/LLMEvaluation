
import json
from evaluate import judge_answer

question = "Explain RAG and give one practical example."

reference_answer = (
    "RAG means Retrieval-Augmented Generation. "
    "It retrieves relevant information and provides "
    "context to an LLM before it generates an answer."
)

model_answer = (
    "RAG means Retrieval-Augmented Generation. "
    "It retrieves relevant information from a knowledge source "
    "and provides that context to an LLM to generate a grounded answer."
)

result = judge_answer(
    question,
    reference_answer,
    model_answer,
)

print(json.dumps(result, indent=2))
print("MODEL ANSWER SENT TO JUDGE:")
print(model_answer)
print("\nJUDGE RESULT:")