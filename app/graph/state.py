from typing import (
    Any,
    Literal,
    TypedDict
)


class InterviewGraphState(
    TypedDict,
    total=False
):
    """
    Shared state passed through the LangGraph workflow.
    """

    action: Literal[
        "retrieve",
        "evaluate",
        "hint",
        "report"
    ]

    company: str
    difficulty: str

    query: str
    k: int

    retrieved_questions: list[
        dict[str, Any]
    ]

    question_id: str
    question: dict[str, Any]

    language: str
    code: str

    visible_only: bool

    judge_result: dict[
        str,
        Any
    ]

    hint: str

    submissions: list[
        dict[str, Any]
    ]

    ai_report: str