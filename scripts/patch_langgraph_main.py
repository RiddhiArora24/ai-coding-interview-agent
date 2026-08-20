from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

file = (
    ROOT
    / "app"
    / "main.py"
)

text = file.read_text(
    encoding="utf-8-sig"
)


# ============================================================
# ADD LANGGRAPH IMPORT
# ============================================================

graph_import = """
from app.graph.interview_graph import (
    evaluate_candidate_code,
    generate_contextual_hint,
    generate_final_ai_report
)

"""


marker = """
from app.interview_service import (
"""


if (
    "generate_contextual_hint"
    not in text
):

    text = text.replace(
        marker,
        graph_import + marker,
        1
    )


# ============================================================
# REPLACE RUN/SUBMIT/HINT EVALUATION
# ============================================================

text = text.replace(
'''    result = run_submission(
        question=question_data,
        code=request.code,
        language=request.language,
        visible_only=True
    )
''',
'''    result = evaluate_candidate_code(
        question=question_data,
        code=request.code,
        language=request.language,
        visible_only=True
    )
'''
)


text = text.replace(
'''    result = run_submission(
        question=question_data,
        code=request.code,
        language=request.language,
        visible_only=False
    )
''',
'''    result = evaluate_candidate_code(
        question=question_data,
        code=request.code,
        language=request.language,
        visible_only=False
    )
'''
)


# ============================================================
# REPLACE DIRECT HINT CALL
# ============================================================

old_hint = '''        hint_text = await generate_hint(
            token=aipipe_token,
            question=question_data,
            code=request.code,
            language=request.language,
            judge_result=result
        )
'''


new_hint = '''        hint_text = await generate_contextual_hint(
            question=question_data,
            code=request.code,
            language=request.language,
            judge_result=result
        )
'''


text = text.replace(
    old_hint,
    new_hint
)


# Static-key version may not contain token argument.
old_hint_two = '''        hint_text = await generate_hint(
            question=question_data,
            code=request.code,
            language=request.language,
            judge_result=result
        )
'''


text = text.replace(
    old_hint_two,
    new_hint
)


# ============================================================
# REPLACE FINAL REPORT CALL
# ============================================================

old_report = '''            ai_report = await generate_report(
                token=aipipe_token,
                company=session["company"],
                difficulty=session[
                    "difficulty"
                ],
                submissions=basic_report[
                    "submissions"
                ]
            )
'''


new_report = '''            ai_report = await generate_final_ai_report(
                company=session["company"],
                difficulty=session[
                    "difficulty"
                ],
                submissions=basic_report[
                    "submissions"
                ]
            )
'''


text = text.replace(
    old_report,
    new_report
)


old_report_two = '''        ai_report = await generate_report(
            company=session["company"],
            difficulty=session[
                "difficulty"
            ],
            submissions=basic_report[
                "submissions"
            ]
        )
'''


new_report_two = '''        ai_report = await generate_final_ai_report(
            company=session["company"],
            difficulty=session[
                "difficulty"
            ],
            submissions=basic_report[
                "submissions"
            ]
        )
'''


text = text.replace(
    old_report_two,
    new_report_two
)


file.write_text(
    text,
    encoding="utf-8"
)


print(
    "FastAPI endpoints patched to use LangGraph."
)