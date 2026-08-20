import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]

load_dotenv(
    ROOT / ".env"
)


AIPIPE_URL = os.getenv(
    "AIPIPE_API_URL",
    "https://aipipe.org/openrouter/v1/chat/completions"
)

MODEL = os.getenv(
    "AIPIPE_MODEL",
    "openai/gpt-4.1-nano"
)


def get_aipipe_key():

    key = os.getenv(
        "AIPIPE_API_KEY",
        ""
    ).strip()

    if (
        not key
        or key.startswith("<")
    ):
        raise ValueError(
            "AIPIPE_API_KEY is missing. "
            "Put your AI Pipe token inside the root .env file."
        )

    return key


async def call_llm(
    messages,
    temperature=0.3
):

    token = get_aipipe_key()

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(
        timeout=45
    ) as client:

        response = await client.post(
            AIPIPE_URL,
            headers=headers,
            json=payload
        )

    if response.status_code >= 400:

        raise RuntimeError(
            "AI Pipe request failed: "
            + response.text[:1000]
        )

    data = response.json()

    try:

        return (
            data["choices"][0]
            ["message"]
            ["content"]
        )

    except Exception:

        raise RuntimeError(
            "Unexpected AI Pipe response: "
            + str(data)[:1000]
        )


async def generate_hint(
    token=None,
    question=None,
    code="",
    language="python",
    judge_result=None
):

    judge_result = (
        judge_result
        or {}
    )

    system = """
You are an expert technical coding interviewer.

Give the candidate ONE useful hint.

Rules:
- Do not reveal the complete solution.
- Do not provide complete code.
- Do not reveal hidden test cases.
- Analyze the candidate's current approach.
- Point toward the likely conceptual mistake.
- Keep the hint concise.
- Maximum 90 words.
"""

    user = f"""
Problem:
{question["problem_statement"]}

Topics:
{", ".join(question["topics"])}

Programming language:
{language}

Candidate code:

{code}

Tests passed:
{judge_result.get("passed", 0)}
out of
{judge_result.get("total", 0)}

Error:
{judge_result.get("error", "No compiler/runtime error")}

Give one helpful interviewer-style hint.
"""

    return await call_llm(
        [
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            }
        ]
    )


async def generate_report(
    token=None,
    company="",
    difficulty="",
    submissions=None
):

    submissions = (
        submissions
        or []
    )

    summary_lines = []

    for item in submissions:

        summary_lines.append(
            (
                f'{item["title"]}: '
                f'{item["passed"]}/{item["total"]} tests passed, '
                f'language={item["language"]}'
            )
        )

    summary = "\n".join(
        summary_lines
    )

    system = """
You are an expert technical interviewer.

Generate a concise coding interview performance report.

Use these sections:

Overall Performance
Strengths
Areas to Improve
Problem Solving
Code Correctness
Recommended Next Steps

Do not invent information.
Base the report only on the supplied interview results.
"""

    user = f"""
Company:
{company}

Difficulty:
{difficulty}

Candidate results:

{summary}
"""

    return await call_llm(
        [
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            }
        ]
    )