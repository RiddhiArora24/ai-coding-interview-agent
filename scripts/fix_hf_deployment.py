import re
from pathlib import Path

root = Path.cwd()

# ---------- accounts.py ----------
accounts_file = root / "app" / "accounts.py"
text = accounts_file.read_text(encoding="utf-8-sig")

if "DATABASE_PATH" not in text:
    pattern = re.compile(
        r'DB_PATH\s*=\s*\(\s*ROOT\s*/\s*"data"\s*/\s*"interview_agent\.db"\s*\)',
        re.MULTILINE,
    )

    replacement = """LOCAL_DB_PATH = (
    ROOT
    / "data"
    / "interview_agent.db"
)

DB_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        str(LOCAL_DB_PATH)
    )
).expanduser()"""

    text, count = pattern.subn(
        replacement,
        text,
        count=1
    )

    if count != 1:
        raise RuntimeError(
            "Could not locate DB_PATH in app/accounts.py"
        )

accounts_file.write_text(
    text,
    encoding="utf-8"
)

# ---------- main.py ----------
main_file = root / "app" / "main.py"
main = main_file.read_text(encoding="utf-8-sig")

# Remove previous copies of our frontend import/mount.
main = re.sub(
    r'\nfrom app\.hf_frontend import mount_frontend\s*\n\s*mount_frontend\(app\)\s*',
    '\n',
    main,
    flags=re.MULTILINE,
)

# Remove orphaned deployment marker.
main = main.replace(
    "# HUGGING_FACE_FRONTEND_SERVING",
    ""
)

main = main.rstrip() + """

# ============================================================
# HUGGING FACE / PRODUCTION FRONTEND
# Keep this after API route registration.
# ============================================================

# HUGGING_FACE_FRONTEND_SERVING
from app.hf_frontend import mount_frontend

mount_frontend(app)
"""

main_file.write_text(
    main,
    encoding="utf-8"
)

print("accounts.py and main.py patched successfully.")