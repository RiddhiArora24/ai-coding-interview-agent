from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# PATCH FRONTEND AUTH
# ============================================================

app_file = ROOT / "frontend" / "src" / "App.jsx"

text = app_file.read_text(
    encoding="utf-8-sig"
)


start_marker = """  // ==========================================================
  // AI PIPE AUTHENTICATION
  // ==========================================================
"""


end_marker = """  // ==========================================================
  // LOAD COMPANIES
  // ==========================================================
"""


if start_marker in text and end_marker in text:

    start = text.index(
        start_marker
    )

    end = text.index(
        end_marker,
        start
    )

    replacement = """  // ==========================================================
  // LOCAL APPLICATION PROFILE
  // AI Pipe API key is stored securely in backend .env
  // ==========================================================

  useEffect(() => {

    setProfile({
      email: "Candidate"
    });

  }, []);


"""

    text = (
        text[:start]
        + replacement
        + text[end:]
    )


app_file.write_text(
    text,
    encoding="utf-8"
)


# ============================================================
# PATCH BACKEND
# ============================================================

main_file = ROOT / "app" / "main.py"

main_text = main_file.read_text(
    encoding="utf-8-sig"
)


# Remove mandatory AI Pipe header check for hints
old_hint_check = '''    if not aipipe_token:

        raise HTTPException(
            status_code=401,
            detail=(
                "AI Pipe token required "
                "for AI-generated hints."
            )
        )

'''

main_text = main_text.replace(
    old_hint_check,
    ""
)


# Make final AI report always use server-side API key
old_report = '''    ai_report = None

    if aipipe_token:

        try:

            ai_report = await generate_report(
                token=aipipe_token,
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
'''


new_report = '''    ai_report = None

    try:

        ai_report = await generate_report(
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
'''


main_text = main_text.replace(
    old_report,
    new_report
)


main_file.write_text(
    main_text,
    encoding="utf-8"
)


print(
    "Frontend AI Pipe redirect removed."
)

print(
    "Backend changed to server-side AI Pipe API key."
)