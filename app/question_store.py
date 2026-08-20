import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "questions.json"


def load_questions():

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


QUESTIONS = load_questions()

QUESTION_MAP = {
    question["id"]: question
    for question in QUESTIONS
}


def get_question(question_id):

    return QUESTION_MAP.get(question_id)


def get_companies():

    return sorted(
        set(
            question["company"]
            for question in QUESTIONS
        )
    )
