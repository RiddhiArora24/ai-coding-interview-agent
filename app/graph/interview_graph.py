from langgraph.graph import (
    END,
    START,
    StateGraph
)

from app.aipipe import (
    generate_hint,
    generate_report
)

from app.graph.state import (
    InterviewGraphState
)

from app.judge import (
    run_submission
)

from app.question_store import (
    get_question
)

from app.rag.retriever import (
    QuestionRetriever
)


_RETRIEVER = None


def get_retriever():

    global _RETRIEVER

    if _RETRIEVER is None:

        _RETRIEVER = (
            QuestionRetriever()
        )

    return _RETRIEVER


# ============================================================
# DISPATCH
# ============================================================

def dispatch_node(
    state: InterviewGraphState
):

    return {}


def route_action(
    state: InterviewGraphState
):

    action = state.get(
        "action"
    )

    if action not in {
        "retrieve",
        "evaluate",
        "hint",
        "report"
    }:

        raise ValueError(
            f"Unknown graph action: {action}"
        )

    return action


# ============================================================
# NODE 1 - LANGCHAIN RAG RETRIEVAL
# ============================================================

def retrieve_questions_node(
    state: InterviewGraphState
):

    company = state[
        "company"
    ]

    difficulty = state[
        "difficulty"
    ]

    query = state.get(
        "query"
    )

    if not query:

        query = (
            f"{company} {difficulty} "
            "coding interview data structures "
            "algorithms problem"
        )


    results = (
        get_retriever()
        .search(
            query=query,
            company=company,
            difficulty=difficulty,
            k=state.get(
                "k",
                4
            )
        )
    )


    return {
        "query": query,
        "retrieved_questions": results
    }


# ============================================================
# NODE 2 - CODE EVALUATION
# ============================================================

def evaluate_code_node(
    state: InterviewGraphState
):

    question = state.get(
        "question"
    )

    if not question:

        question = get_question(
            state[
                "question_id"
            ]
        )


    if not question:

        raise ValueError(
            "Question was not found."
        )


    result = run_submission(
        question=question,
        code=state["code"],
        language=state["language"],
        visible_only=state.get(
            "visible_only",
            False
        )
    )


    return {
        "question": question,
        "judge_result": result
    }


# ============================================================
# NODE 3 - CONTEXTUAL AI HINT
# ============================================================

async def generate_hint_node(
    state: InterviewGraphState
):

    question = state.get(
        "question"
    )

    if not question:

        question = get_question(
            state[
                "question_id"
            ]
        )


    result = state.get(
        "judge_result"
    )


    if result is None:

        result = run_submission(
            question=question,
            code=state["code"],
            language=state["language"],
            visible_only=False
        )


    hint = await generate_hint(
        question=question,
        code=state["code"],
        language=state["language"],
        judge_result=result
    )


    return {
        "question": question,
        "judge_result": result,
        "hint": hint
    }


# ============================================================
# NODE 4 - FINAL AI REPORT
# ============================================================

async def generate_report_node(
    state: InterviewGraphState
):

    report = await generate_report(
        company=state[
            "company"
        ],
        difficulty=state[
            "difficulty"
        ],
        submissions=state.get(
            "submissions",
            []
        )
    )


    return {
        "ai_report": report
    }


# ============================================================
# GRAPH DEFINITION
# ============================================================

workflow = StateGraph(
    InterviewGraphState
)


workflow.add_node(
    "dispatch",
    dispatch_node
)

workflow.add_node(
    "retrieve_questions",
    retrieve_questions_node
)

workflow.add_node(
    "evaluate_code",
    evaluate_code_node
)

workflow.add_node(
    "generate_hint",
    generate_hint_node
)

workflow.add_node(
    "generate_report",
    generate_report_node
)


workflow.add_edge(
    START,
    "dispatch"
)


workflow.add_conditional_edges(
    "dispatch",
    route_action,
    {
        "retrieve": (
            "retrieve_questions"
        ),
        "evaluate": (
            "evaluate_code"
        ),
        "hint": (
            "generate_hint"
        ),
        "report": (
            "generate_report"
        )
    }
)


workflow.add_edge(
    "retrieve_questions",
    END
)

workflow.add_edge(
    "evaluate_code",
    END
)

workflow.add_edge(
    "generate_hint",
    END
)

workflow.add_edge(
    "generate_report",
    END
)


interview_graph = (
    workflow.compile()
)


# ============================================================
# APPLICATION HELPERS
# ============================================================

def retrieve_interview_questions(
    company,
    difficulty,
    k=4
):

    state = (
        interview_graph.invoke({
            "action": "retrieve",
            "company": company,
            "difficulty": difficulty,
            "k": k
        })
    )

    return state[
        "retrieved_questions"
    ]


def evaluate_candidate_code(
    question,
    code,
    language,
    visible_only=False
):

    state = (
        interview_graph.invoke({
            "action": "evaluate",
            "question_id": question[
                "id"
            ],
            "question": question,
            "code": code,
            "language": language,
            "visible_only": (
                visible_only
            )
        })
    )

    return state[
        "judge_result"
    ]


async def generate_contextual_hint(
    question,
    code,
    language,
    judge_result=None
):

    state = (
        await interview_graph.ainvoke({
            "action": "hint",
            "question_id": question[
                "id"
            ],
            "question": question,
            "code": code,
            "language": language,
            "judge_result": (
                judge_result
            )
        })
    )

    return state[
        "hint"
    ]


async def generate_final_ai_report(
    company,
    difficulty,
    submissions
):

    state = (
        await interview_graph.ainvoke({
            "action": "report",
            "company": company,
            "difficulty": difficulty,
            "submissions": submissions
        })
    )

    return state[
        "ai_report"
    ]