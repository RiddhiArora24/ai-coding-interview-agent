from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

file = ROOT / "app" / "main.py"

text = file.read_text(
    encoding="utf-8-sig"
)


marker = (
    "from app.accounts import "
    "router as accounts_router"
)


if marker not in text:

    text += """

# ============================================================
# ACCOUNT / REPORT ROUTES
# ============================================================

from app.accounts import router as accounts_router

app.include_router(
    accounts_router
)
"""


file.write_text(
    text,
    encoding="utf-8"
)

print(
    "Account routes registered."
)