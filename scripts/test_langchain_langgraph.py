import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT)
)


from app.graph.interview_graph import (
    evaluate_candidate_code,
    interview_graph,
    retrieve_interview_questions
)


print()
print("=" * 68)
print("LANGCHAIN + LANGGRAPH INTEGRATION TEST")
print("=" * 68)


# ============================================================
# LANGCHAIN / FAISS RETRIEVAL THROUGH LANGGRAPH
# ============================================================

results = retrieve_interview_questions(
    company="Google",
    difficulty="Hard",
    k=4
)


print()
print(
    "LangGraph retrieval results:"
)

for item in results:

    print(
        "-",
        item["title"],
        "|",
        item["company"],
        "|",
        item["difficulty"],
        "| score:",
        item["score"]
    )


assert len(results) == 4

assert all(
    item["company"] == "Google"
    for item in results
)

assert all(
    item["difficulty"] == "Hard"
    for item in results
)


# ============================================================
# LANGGRAPH CODE-EVALUATION NODE
# ============================================================

from app.question_store import (
    get_question
)


question = get_question(
    "amazon_001"
)


code = """
def solve(nums, target):

    seen = {}

    for i, value in enumerate(nums):

        need = target - value

        if need in seen:
            return [seen[need], i]

        seen[value] = i

    return []
"""


judge = evaluate_candidate_code(
    question=question,
    code=code,
    language="python",
    visible_only=False
)


print()
print(
    "LangGraph code evaluation:"
)

print(
    judge["passed"],
    "/",
    judge["total"],
    "tests passed"
)


assert judge["passed"] == 5


# ============================================================
# SHOW LANGGRAPH STRUCTURE
# ============================================================

print()
print(
    "LangGraph workflow:"
)

print(
    interview_graph
    .get_graph()
    .draw_mermaid()
)


print()
print("=" * 68)
print("LANGCHAIN + LANGGRAPH ARE WORKING")
print("=" * 68)