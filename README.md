<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=AI%20Coding%20Interview%20Agent&fontSize=40&fontColor=fff&animation=fadeIn&desc=Practice.%20Improve.%20Get%20hired.&descAlignY=62&descSize=18)

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&pause=1000&color=61DAFB&center=true&vCenter=true&width=720&lines=Company-targeted+mock+technical+interviews;LangChain+RAG+%2B+LangGraph+Workflow;FAISS+%2B+Live+Python%2FC%2B%2B+Execution;AI+Hints+that+Never+Reveal+the+Answer)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C)
![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-8B5CF6)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange)
![JWT](https://img.shields.io/badge/Auth-JWT-black?logo=jsonwebtokens)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

An AI-powered mock interview platform where candidates choose a company and difficulty, solve four semantically retrieved coding questions in Python or C++, run code against test cases, request contextual AI hints, and receive an AI-generated performance report with persistent interview history.

**60 curated questions · 5 companies · 300 test cases · Python + C++ · LangChain RAG · LangGraph orchestration**

---

## ✨ Features

- 🔐 **Secure authentication** — JWT sessions with PBKDF2-HMAC-SHA256 password hashing
- 🧠 **LangChain RAG** — `Document` + `FastEmbedEmbeddings` + FAISS semantic retrieval
- 🕸️ **LangGraph workflow** — routes retrieval, code evaluation, hint generation, and final reporting
- 💻 **Real code execution** — Python subprocess and C++17 via `g++`
- 🧪 **Visible + full test evaluation** — Run uses visible tests; Submit evaluates the complete test suite
- 💡 **AI hints, not answers** — model receives candidate code and judge context without revealing full solutions
- 📊 **AI performance reports** — score, strengths, weaknesses, and recommended next steps
- 🕘 **Per-user history** — reports are persisted in SQLite and scoped by `user_id`

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite, Monaco Editor |
| Backend | FastAPI (Python) |
| Workflow Orchestration | **LangGraph `StateGraph`** |
| RAG Framework | **LangChain** |
| Retrieval | LangChain FAISS + `BAAI/bge-small-en-v1.5` |
| Embeddings | FastEmbed via `FastEmbedEmbeddings` |
| AI Layer | AI Pipe → OpenRouter |
| Auth | JWT + PBKDF2-HMAC-SHA256 |
| Database | SQLite |
| Execution | Python `subprocess` / `g++` (C++17) |

## 🔄 Interview Workflow

```mermaid
flowchart LR
    A[Login / Signup] --> B[Select Company]
    B --> C[Select Difficulty]
    C --> D[Start Interview]
    D --> E[LangGraph]
    E --> F[LangChain + FAISS]
    F --> G[Retrieve 4 Questions]
    G --> H[Code in Python / C++]
    H --> I[Run / Submit]
    I --> J[Code Judge]
    J --> K{Need Hint?}
    K -- Yes --> L[LangGraph Hint Node]
    L --> M[AI Pipe → OpenRouter]
    M --> H
    K -- No --> N[Next Question]
    N --> O[Finish Interview]
    O --> P[LangGraph Report Node]
    P --> M
    P --> Q[Final Report]
    Q --> R[(SQLite History)]
```

## 📐 High-Level Design

```mermaid
graph TD
    A["React + Vite<br/>Monaco Editor"] -->|JWT + REST| B[FastAPI]

    B --> AUTH[Auth Service]
    AUTH --> DB[("SQLite")]

    B --> LG["LangGraph<br/>Interview Workflow"]

    LG --> R["retrieve_questions"]
    LG --> EV["evaluate_code"]
    LG --> HN["generate_hint"]
    LG --> RP["generate_report"]

    R --> LC["LangChain RAG"]
    LC --> EMB["FastEmbedEmbeddings<br/>bge-small-en-v1.5"]
    EMB --> F["FAISS Vector Store<br/>60 Questions"]

    EV --> J[Code Judge]
    J --> PY["Python subprocess"]
    J --> CPP["g++ / C++17"]

    HN --> AI[AI Pipe]
    RP --> AI
    AI --> OR[OpenRouter LLM]

    B --> DB

    style A fill:#61DAFB,color:#000
    style B fill:#009688,color:#fff
    style LG fill:#8b5cf6,color:#fff
    style LC fill:#1C3C3C,color:#fff
    style F fill:#f97316,color:#fff
    style OR fill:#7c3aed,color:#fff
```

### Why LangChain?

LangChain owns the RAG layer:

```text
questions.json
      ↓
LangChain Documents
      ↓
FastEmbedEmbeddings
      ↓
FAISS Vector Store
      ↓
Company + Difficulty Filter
      ↓
Top 4 Relevant Questions
```

Only candidate-safe fields are embedded: **title, company, difficulty, topics, and problem statement**. Solutions and hidden tests are excluded from the vector store.

### Why LangGraph?

LangGraph orchestrates the actual interview workflow through a stateful graph:

```text
START
  ↓
dispatch
  ├── retrieve_questions → LangChain + FAISS
  ├── evaluate_code      → Python/C++ Judge
  ├── generate_hint      → AI Pipe/OpenRouter
  └── generate_report    → AI Pipe/OpenRouter
  ↓
END
```

This keeps deterministic operations such as code judging separate from LLM-based tasks such as hints and performance feedback.

## ⚡ Quick Start

```bash
git clone <your-repo-url>
cd ai-coding-interview-agent

# Backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

# Add your AI Pipe key + JWT secret to .env

python -m app.rag.build_index
python scripts/test_langchain_langgraph.py
python -m uvicorn app.main:app --reload

# Frontend - new terminal
cd frontend
npm install
npm run dev
```

Backend docs:

```text
http://127.0.0.1:8000/docs
```

Frontend:

```text
http://localhost:5173
```

## 🔌 API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/signup` | Create account |
| POST | `/api/auth/login` | Authenticate user |
| GET | `/api/auth/me` | Get logged-in user |
| POST | `/api/interviews/start` | LangGraph → LangChain/FAISS → retrieve 4 questions |
| GET | `/api/interviews/{id}/questions/{pos}` | Fetch interview question |
| POST | `.../run` | Evaluate visible tests |
| POST | `.../submit` | Evaluate complete test suite |
| POST | `.../hint` | LangGraph → contextual AI hint |
| POST | `.../finish` | LangGraph → score + AI report |
| GET | `.../solutions/{pos}` | View solution after interview |
| POST | `/api/reports` | Persist completed report |
| GET | `/api/reports` | Current user's interview history |

## 📂 Project Structure

```text
ai-coding-interview-agent/
 ├── app/
 │   ├── main.py                 # FastAPI entrypoint
 │   ├── accounts.py             # JWT auth + SQLite reports
 │   ├── interview_service.py    # Interview sessions
 │   ├── judge.py                # Python/C++ execution
 │   ├── aipipe.py               # AI Pipe / OpenRouter client
 │   ├── starter_code.py
 │   ├── question_store.py
 │   │
 │   ├── graph/
 │   │   ├── state.py            # LangGraph shared state
 │   │   └── interview_graph.py  # StateGraph workflow
 │   │
 │   └── rag/
 │       ├── embeddings.py       # LangChain FastEmbed wrapper
 │       ├── build_index.py      # LangChain FAISS builder
 │       └── retriever.py        # Semantic retrieval
 │
 ├── data/
 │   ├── questions.json          # 60 curated problems
 │   └── faiss/
 │       ├── langchain_index/
 │       │   ├── index.faiss
 │       │   └── index.pkl
 │       ├── documents.json
 │       └── config.json
 │
 ├── frontend/
 │   └── src/
 │       ├── App.jsx             # Login + history
 │       ├── InterviewApp.jsx    # Interview UI
 │       ├── api.js
 │       └── styles.css
 │
 ├── scripts/
 │   ├── seed_data.py
 │   ├── test_retrieval.py
 │   └── test_langchain_langgraph.py
 │
 ├── requirements.txt
 ├── .env.example
 └── README.md
```

## 🧠 Dataset

| Company | Easy | Medium | Hard | Total |
|---|---:|---:|---:|---:|
| Amazon | 4 | 4 | 4 | 12 |
| Google | 4 | 4 | 4 | 12 |
| Microsoft | 4 | 4 | 4 | 12 |
| Meta | 4 | 4 | 4 | 12 |
| Goldman Sachs | 4 | 4 | 4 | 12 |
| **Total** | **20** | **20** | **20** | **60** |

Each problem contains **5 test cases**, giving **300 total test cases**.

Company labels are curated practice-targeting labels and do not claim that every exact problem was historically asked by that company.

## 🔐 Environment

Create `.env` from `.env.example`:

```env
AIPIPE_API_KEY=your_aipipe_key
AIPIPE_API_URL=https://aipipe.org/openrouter/v1/chat/completions
AIPIPE_MODEL=openrouter/free

JWT_SECRET_KEY=your_long_random_secret
```

> Never commit `.env`. AI credentials remain entirely on the backend.

## 🔒 Security Notes

- Passwords are hashed with **PBKDF2-HMAC-SHA256** and a unique salt.
- JWT protects authenticated application sessions.
- AI Pipe credentials never reach the React frontend.
- Reports are queried using the authenticated `user_id`.
- Solutions and hidden test cases are excluded from RAG embeddings.
- The LLM provides hints/reports; **the deterministic judge decides correctness**.
- ⚠️ Candidate code currently runs in local subprocesses. This is suitable for local/portfolio use, but public production deployment should use Docker, Firecracker, or another isolated execution sandbox.

## 🎯 Interview Talking Point

> **LangChain handles the RAG layer — document creation, FastEmbed embeddings, FAISS vector storage, metadata filtering, and semantic retrieval. LangGraph orchestrates the interview workflow — retrieval, deterministic code evaluation, contextual hint generation, and final AI reporting.**

## 📄 License

MIT — see [LICENSE](./LICENSE).

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer)

</div>
