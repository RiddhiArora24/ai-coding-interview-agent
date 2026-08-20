from typing import Literal

from fastapi import (
    FastAPI,
    Header,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import (
    BaseModel,
    Field
)


from app.aipipe import (
    generate_hint,
    generate_report
)

from app.graph.interview_graph import (
    evaluate_candidate_code,
    generate_contextual_hint,
    generate_final_ai_report
)


from app.interview_service import (
    build_basic_report,
    create_interview,
    get_session,
    get_session_question,
    remaining_seconds,
    save_submission
)

from app.judge import (
    run_submission
)

from app.question_store import (
    get_companies
)

from app.starter_code import (
    get_starter_code
)


app = FastAPI(
    title="AI Coding Interview Agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


class StartInterviewRequest(
    BaseModel
):

    company: str

    difficulty: Literal[
        "Easy",
        "Medium",
        "Hard"
    ]


class CodeRequest(
    BaseModel
):

    language: Literal[
        "python",
        "cpp"
    ]

    code: str = Field(
        min_length=1
    )


def require_session(
    session_id
):

    session = get_session(
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    return session


def public_question(
    question,
    position
):

    starters = get_starter_code(
        question
    )

    visible_cases = []

    for case in question[
        "test_cases"
    ][:2]:

        visible_cases.append({
            "input": case["input"],
            "expected": case["expected"]
        })

    return {
        "position": position,
        "total_questions": 4,
        "id": question["id"],
        "title": question["title"],
        "company": question["company"],
        "difficulty": question["difficulty"],
        "topics": question["topics"],
        "problem_statement": question[
            "problem_statement"
        ],
        "visible_test_cases": visible_cases,
        "starter_code": starters
    }


@app.get(
    "/api/health"
)
def health():

    return {
        "status": "ok",
        "service": "AI Coding Interview Agent"
    }


@app.get(
    "/api/companies"
)
def companies():

    return {
        "companies": get_companies(),
        "difficulties": [
            "Easy",
            "Medium",
            "Hard"
        ]
    }


@app.post(
    "/api/interviews/start"
)
def start_interview(
    request: StartInterviewRequest
):

    valid_companies = get_companies()

    if request.company not in valid_companies:

        raise HTTPException(
            status_code=400,
            detail="Invalid company."
        )

    try:

        session = create_interview(
            company=request.company,
            difficulty=request.difficulty
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    return {
        "session_id": session["id"],
        "company": session["company"],
        "difficulty": session["difficulty"],
        "question_count": 4,
        "duration_seconds": session[
            "duration_seconds"
        ]
    }


@app.get(
    "/api/interviews/{session_id}"
)
def interview_status(
    session_id: str
):

    session = require_session(
        session_id
    )

    return {
        "session_id": session["id"],
        "company": session["company"],
        "difficulty": session["difficulty"],
        "submitted": len(
            session["submissions"]
        ),
        "question_count": 4,
        "remaining_seconds": remaining_seconds(
            session
        ),
        "finished": session["finished"]
    }


@app.get(
    "/api/interviews/{session_id}/questions/{position}"
)
def question(
    session_id: str,
    position: int
):

    session = require_session(
        session_id
    )

    question_data = get_session_question(
        session,
        position
    )

    if not question_data:

        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    response = public_question(
        question_data,
        position
    )

    response["remaining_seconds"] = (
        remaining_seconds(
            session
        )
    )

    response["already_submitted"] = (
        question_data["id"]
        in session["submissions"]
    )

    return response


@app.post(
    "/api/interviews/{session_id}/questions/{position}/run"
)
def run_code(
    session_id: str,
    position: int,
    request: CodeRequest
):

    session = require_session(
        session_id
    )

    question_data = get_session_question(
        session,
        position
    )

    if not question_data:

        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    result = evaluate_candidate_code(
        question=question_data,
        code=request.code,
        language=request.language,
        visible_only=True
    )

    return result


@app.post(
    "/api/interviews/{session_id}/questions/{position}/submit"
)
def submit_code(
    session_id: str,
    position: int,
    request: CodeRequest
):

    session = require_session(
        session_id
    )

    question_data = get_session_question(
        session,
        position
    )

    if not question_data:

        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    result = evaluate_candidate_code(
        question=question_data,
        code=request.code,
        language=request.language,
        visible_only=False
    )

    save_submission(
        session=session,
        question=question_data,
        language=request.language,
        code=request.code,
        result=result
    )

    return {
        "question_id": question_data["id"],
        "title": question_data["title"],
        "passed": result["passed"],
        "total": result["total"],
        "success": result["success"],
        "compile_error": result.get(
            "compile_error",
            False
        ),
        "compiler_missing": result.get(
            "compiler_missing",
            False
        ),
        "error": result.get(
            "error"
        ),
        "interview_complete": session[
            "finished"
        ],
        "submitted_questions": len(
            session["submissions"]
        )
    }


@app.post(
    "/api/interviews/{session_id}/questions/{position}/hint"
)
async def hint(
    session_id: str,
    position: int,
    request: CodeRequest,
    aipipe_token: str | None = Header(
        default=None,
        alias="X-AIPipe-Token"
    )
):

    session = require_session(
        session_id
    )

    question_data = get_session_question(
        session,
        position
    )

    if not question_data:

        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    result = evaluate_candidate_code(
        question=question_data,
        code=request.code,
        language=request.language,
        visible_only=False
    )

    if result["success"]:

        return {
            "hint": (
                "Your solution already passes "
                "all available test cases."
            )
        }

    try:

        hint_text = await generate_contextual_hint(
            question=question_data,
            code=request.code,
            language=request.language,
            judge_result=result
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )

    return {
        "hint": hint_text,
        "tests_passed": result["passed"],
        "total_tests": result["total"]
    }


@app.post(
    "/api/interviews/{session_id}/finish"
)
async def finish(
    session_id: str,
    aipipe_token: str | None = Header(
        default=None,
        alias="X-AIPipe-Token"
    )
):

    session = require_session(
        session_id
    )

    if len(
        session["submissions"]
    ) < 4:

        raise HTTPException(
            status_code=400,
            detail=(
                "Submit all four questions "
                "before finishing."
            )
        )

    session["finished"] = True

    basic_report = build_basic_report(
        session
    )

    ai_report = None

    try:

        ai_report = await generate_final_ai_report(
            company=session["company"],
            difficulty=session[
                "difficulty"
            ],
            submissions=basic_report[
                "submissions"
            ]
        )

    except Exception as error:

        ai_report = (
            "AI report unavailable: "
            + str(error)
        )

    return {
        **basic_report,
        "ai_report": ai_report
    }


@app.get(
    "/api/interviews/{session_id}/solutions/{position}"
)
def solution(
    session_id: str,
    position: int
):

    session = require_session(
        session_id
    )

    if not session["finished"]:

        raise HTTPException(
            status_code=403,
            detail=(
                "Solutions are available "
                "only after the interview."
            )
        )

    question_data = get_session_question(
        session,
        position
    )

    if not question_data:

        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    return {
        "id": question_data["id"],
        "title": question_data["title"],
        "solution": question_data["solution"]
    }


# ============================================================
# ACCOUNT / REPORT ROUTES
# ============================================================

from app.accounts import router as accounts_router

app.include_router(
    accounts_router
)

# ============================================================
# HUGGING FACE / PRODUCTION FRONTEND
# Keep this after API route registration.
# ============================================================

# ============================================================
# HUGGING FACE / PRODUCTION FRONTEND
# Keep this after API route registration.
# ============================================================

# HUGGING_FACE_FRONTEND_SERVING
from app.hf_frontend import mount_frontend

mount_frontend(app)
