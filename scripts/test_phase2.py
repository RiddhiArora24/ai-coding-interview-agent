import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT)
)


from app.judge import run_submission
from app.question_store import get_question
from app.interview_service import create_interview


print()
print("=" * 60)
print("PHASE 2 SMOKE TEST")
print("=" * 60)


# ============================================================
# TEST PYTHON JUDGE
# ============================================================

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


result = run_submission(
    question=question,
    code=code,
    language="python",
    visible_only=False
)


print()
print("Python judge:")
print(
    result["passed"],
    "/",
    result["total"],
    "tests passed"
)

assert result["passed"] == 5


# ============================================================
# TEST INTERVIEW CREATION
# ============================================================

session = create_interview(
    company="Amazon",
    difficulty="Medium"
)


print()
print("Interview session created:")
print(
    session["id"]
)

print(
    "Questions:",
    session["question_ids"]
)

assert len(
    session["question_ids"]
) == 4


print()
print("=" * 60)
print("PHASE 2 BACKEND IS WORKING")
print("=" * 60)
