import time
import uuid

from app.graph.interview_graph import (
    retrieve_interview_questions
)

from app.question_store import (
    get_question
)


SESSIONS = {}


def create_interview(
    company,
    difficulty
):
    """
    Interview question selection is now executed through
    the LangGraph workflow.

    LangGraph node:
        retrieve_questions

    which internally uses:
        LangChain -> FastEmbed -> FAISS
    """

    results = (
        retrieve_interview_questions(
            company=company,
            difficulty=difficulty,
            k=4
        )
    )


    if len(results) < 4:

        raise ValueError(
            "Not enough matching questions found."
        )


    question_ids = [
        result["id"]
        for result in results
    ]


    session_id = str(
        uuid.uuid4()
    )


    SESSIONS[
        session_id
    ] = {
        "id": session_id,
        "company": company,
        "difficulty": difficulty,
        "question_ids": question_ids,
        "submissions": {},
        "started_at": time.time(),
        "duration_seconds": 60 * 60,
        "finished": False
    }


    return SESSIONS[
        session_id
    ]


def get_session(
    session_id
):

    return SESSIONS.get(
        session_id
    )


def get_session_question(
    session,
    position
):

    if (
        position < 1
        or position > 4
    ):

        return None


    question_id = (
        session[
            "question_ids"
        ][position - 1]
    )


    return get_question(
        question_id
    )


def remaining_seconds(
    session
):

    elapsed = (
        time.time()
        - session[
            "started_at"
        ]
    )


    remaining = (
        session[
            "duration_seconds"
        ]
        - int(elapsed)
    )


    return max(
        0,
        remaining
    )


def save_submission(
    session,
    question,
    language,
    code,
    result
):

    session[
        "submissions"
    ][question["id"]] = {
        "question_id": question["id"],
        "title": question["title"],
        "language": language,
        "code": code,
        "passed": result["passed"],
        "total": result["total"],
        "success": result["success"]
    }


    if len(
        session[
            "submissions"
        ]
    ) >= 4:

        session[
            "finished"
        ] = True


def build_basic_report(
    session
):

    submissions = list(
        session[
            "submissions"
        ].values()
    )


    total_tests = sum(
        item["total"]
        for item in submissions
    )


    passed_tests = sum(
        item["passed"]
        for item in submissions
    )


    solved = sum(
        1
        for item in submissions
        if item["success"]
    )


    score = 0


    if total_tests:

        score = round(
            passed_tests
            / total_tests
            * 100,
            1
        )


    return {
        "company": session[
            "company"
        ],
        "difficulty": session[
            "difficulty"
        ],
        "questions_attempted": len(
            submissions
        ),
        "questions_fully_solved": (
            solved
        ),
        "tests_passed": passed_tests,
        "total_tests": total_tests,
        "score_percent": score,
        "submissions": submissions
    }