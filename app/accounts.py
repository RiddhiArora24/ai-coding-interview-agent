import hashlib
import hmac
import json
import os
import secrets
import sqlite3

from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt

from dotenv import load_dotenv

from fastapi import (
    APIRouter,
    Header,
    HTTPException
)

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


ROOT = Path(__file__).resolve().parents[1]

load_dotenv(
    ROOT / ".env"
)


DB_PATH = (
    ROOT
    / "data"
    / "interview_agent.db"
)


JWT_SECRET = os.getenv(
    "JWT_SECRET_KEY",
    ""
)


JWT_ALGORITHM = "HS256"

router = APIRouter()


# ============================================================
# DATABASE
# ============================================================

def connection():

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    conn.row_factory = (
        sqlite3.Row
    )

    return conn


def init_database():

    conn = connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score_percent REAL NOT NULL,
            questions_fully_solved INTEGER NOT NULL,
            questions_attempted INTEGER NOT NULL,
            tests_passed INTEGER NOT NULL,
            total_tests INTEGER NOT NULL,
            ai_report TEXT,
            report_json TEXT NOT NULL,
            created_at TEXT NOT NULL,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
        """
    )

    conn.commit()

    conn.close()


init_database()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(
    password
):

    salt = secrets.token_bytes(
        16
    )

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        180000
    )

    return (
        salt.hex()
        + ":"
        + digest.hex()
    )


def verify_password(
    password,
    stored
):

    try:

        salt_hex, digest_hex = (
            stored.split(
                ":",
                1
            )
        )

        salt = bytes.fromhex(
            salt_hex
        )

        expected = bytes.fromhex(
            digest_hex
        )

        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            180000
        )

        return hmac.compare_digest(
            actual,
            expected
        )

    except Exception:

        return False


# ============================================================
# JWT
# ============================================================

def make_token(
    user
):

    if not JWT_SECRET:

        raise RuntimeError(
            "JWT_SECRET_KEY is missing."
        )

    now = datetime.now(
        timezone.utc
    )

    payload = {
        "sub": str(
            user["id"]
        ),
        "email": user["email"],
        "name": user["name"],
        "iat": now,
        "exp": now + timedelta(
            days=7
        )
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )


def get_current_user(
    authorization: str | None = Header(
        default=None
    )
):

    if (
        not authorization
        or not authorization.startswith(
            "Bearer "
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Login required."
        )

    token = authorization[
        7:
    ].strip()

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[
                JWT_ALGORITHM
            ]
        )

        user_id = int(
            payload["sub"]
        )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid or expired login session."
            )
        )

    conn = connection()

    row = conn.execute(
        """
        SELECT
            id,
            name,
            email,
            created_at
        FROM users
        WHERE id = ?
        """,
        (
            user_id,
        )
    ).fetchone()

    conn.close()

    if not row:

        raise HTTPException(
            status_code=401,
            detail="User no longer exists."
        )

    return dict(
        row
    )


# ============================================================
# REQUEST MODELS
# ============================================================

class SignupRequest(
    BaseModel
):

    name: str = Field(
        min_length=2,
        max_length=80
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(
    BaseModel
):

    email: EmailStr

    password: str


# ============================================================
# SIGNUP
# ============================================================

@router.post(
    "/api/auth/signup"
)
def signup(
    request: SignupRequest
):

    name = request.name.strip()

    email = (
        request.email
        .strip()
        .lower()
    )

    conn = connection()

    existing = conn.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (
            email,
        )
    ).fetchone()

    if existing:

        conn.close()

        raise HTTPException(
            status_code=409,
            detail=(
                "An account with this email "
                "already exists."
            )
        )

    password_hash = hash_password(
        request.password
    )

    created_at = (
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    cursor = conn.execute(
        """
        INSERT INTO users (
            name,
            email,
            password_hash,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            email,
            password_hash,
            created_at
        )
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    user = {
        "id": user_id,
        "name": name,
        "email": email
    }

    return {
        "token": make_token(
            user
        ),
        "user": user
    }


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/api/auth/login"
)
def login(
    request: LoginRequest
):

    email = (
        request.email
        .strip()
        .lower()
    )

    conn = connection()

    row = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (
            email,
        )
    ).fetchone()

    conn.close()

    if not row:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid email or password."
            )
        )

    user = dict(
        row
    )

    if not verify_password(
        request.password,
        user["password_hash"]
    ):

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid email or password."
            )
        )

    public_user = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }

    return {
        "token": make_token(
            public_user
        ),
        "user": public_user
    }


# ============================================================
# CURRENT USER
# ============================================================

@router.get(
    "/api/auth/me"
)
def me(
    authorization: str | None = Header(
        default=None
    )
):

    return get_current_user(
        authorization
    )


# ============================================================
# SAVE REPORT
# ============================================================

@router.post(
    "/api/reports"
)
def save_report(
    report: dict,
    authorization: str | None = Header(
        default=None
    )
):

    user = get_current_user(
        authorization
    )

    created_at = (
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    conn = connection()

    cursor = conn.execute(
        """
        INSERT INTO reports (
            user_id,
            company,
            difficulty,
            score_percent,
            questions_fully_solved,
            questions_attempted,
            tests_passed,
            total_tests,
            ai_report,
            report_json,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user["id"],
            report.get(
                "company",
                "Unknown"
            ),
            report.get(
                "difficulty",
                "Unknown"
            ),
            float(
                report.get(
                    "score_percent",
                    0
                )
            ),
            int(
                report.get(
                    "questions_fully_solved",
                    0
                )
            ),
            int(
                report.get(
                    "questions_attempted",
                    0
                )
            ),
            int(
                report.get(
                    "tests_passed",
                    0
                )
            ),
            int(
                report.get(
                    "total_tests",
                    0
                )
            ),
            report.get(
                "ai_report"
            ),
            json.dumps(
                report
            ),
            created_at
        )
    )

    conn.commit()

    report_id = cursor.lastrowid

    conn.close()

    return {
        "saved": True,
        "report_id": report_id
    }


# ============================================================
# REPORT HISTORY
# ============================================================

@router.get(
    "/api/reports"
)
def history(
    authorization: str | None = Header(
        default=None
    )
):

    user = get_current_user(
        authorization
    )

    conn = connection()

    rows = conn.execute(
        """
        SELECT
            id,
            company,
            difficulty,
            score_percent,
            questions_fully_solved,
            questions_attempted,
            tests_passed,
            total_tests,
            ai_report,
            report_json,
            created_at
        FROM reports
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (
            user["id"],
        )
    ).fetchall()

    conn.close()

    reports = []

    for row in rows:

        item = dict(
            row
        )

        try:

            item["details"] = json.loads(
                item["report_json"]
            )

        except Exception:

            item["details"] = {}

        item.pop(
            "report_json",
            None
        )

        reports.append(
            item
        )

    return {
        "reports": reports
    }