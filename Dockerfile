# ============================================================
# Stage 1 - React production build
# ============================================================

FROM node:22-bookworm-slim AS frontend-builder

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


# ============================================================
# Stage 2 - FastAPI / LangChain / LangGraph
# ============================================================

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860 \
    HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    FASTEMBED_CACHE_DIR=/home/user/.cache/fastembed \
    DATABASE_PATH=/data/interview_agent.db

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        g++ \
        libgomp1 \
        curl && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user && \
    mkdir -p /data && \
    chown -R user:user /data

USER user
WORKDIR /home/user/app

COPY --chown=user:user requirements.txt ./

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY --chown=user:user . .

COPY --from=frontend-builder --chown=user:user \
    /frontend/dist \
    /home/user/app/frontend/dist

RUN mkdir -p "$FASTEMBED_CACHE_DIR" && \
    python -c "from app.rag.embeddings import get_embeddings; e=get_embeddings(); e.embed_query('deployment warmup'); print('FastEmbed model cached')"

EXPOSE 7860

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
