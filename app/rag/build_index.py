import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from app.rag.embeddings import (
    MODEL_NAME,
    get_embeddings
)


ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    ROOT
    / "data"
    / "questions.json"
)

FAISS_ROOT = (
    ROOT
    / "data"
    / "faiss"
)

INDEX_DIR = (
    FAISS_ROOT
    / "langchain_index"
)

DOCUMENTS_FILE = (
    FAISS_ROOT
    / "documents.json"
)

CONFIG_FILE = (
    FAISS_ROOT
    / "config.json"
)


def searchable_text(
    question
):
    """
    Candidate-safe content only.

    Solutions, hints and hidden tests are deliberately
    excluded from the vector database.
    """

    topics = ", ".join(
        question["topics"]
    )

    return f"""
Title: {question["title"]}
Company: {question["company"]}
Difficulty: {question["difficulty"]}
Topics: {topics}

Problem:
{question["problem_statement"]}
""".strip()


def question_to_document(
    question
):

    return Document(
        page_content=searchable_text(
            question
        ),
        metadata={
            "question_id": question["id"],
            "title": question["title"],
            "company": question["company"],
            "difficulty": question["difficulty"],
            "topics": question["topics"]
        }
    )


def build_index():

    print()
    print("=" * 65)
    print("LANGCHAIN + FAISS INDEX BUILDER")
    print("=" * 65)

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        questions = json.load(
            file
        )

    if not questions:

        raise ValueError(
            "No questions were found."
        )

    documents = [
        question_to_document(
            question
        )
        for question in questions
    ]

    print(
        f"Questions loaded : {len(questions)}"
    )

    print(
        f"LangChain docs   : {len(documents)}"
    )

    print(
        f"Embedding model  : {MODEL_NAME}"
    )

    print()
    print(
        "Generating embeddings through "
        "LangChain FastEmbedEmbeddings..."
    )

    embeddings = get_embeddings()

    vector_store = (
        FAISS.from_documents(
            documents,
            embeddings
        )
    )

    INDEX_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    vector_store.save_local(
        str(INDEX_DIR)
    )


    # --------------------------------------------------------
    # Save candidate-safe document metadata for inspection
    # --------------------------------------------------------

    safe_documents = []

    for document in documents:

        safe_documents.append({
            "id": document.metadata[
                "question_id"
            ],
            "company": document.metadata[
                "company"
            ],
            "difficulty": document.metadata[
                "difficulty"
            ],
            "title": document.metadata[
                "title"
            ],
            "topics": document.metadata[
                "topics"
            ],
            "text": document.page_content
        })


    with open(
        DOCUMENTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            safe_documents,
            file,
            indent=2,
            ensure_ascii=False
        )


    config = {
        "framework": "LangChain",
        "vector_store": "FAISS",
        "embedding_provider": (
            "LangChain FastEmbedEmbeddings"
        ),
        "embedding_model": MODEL_NAME,
        "documents": len(documents),
        "index_directory": (
            "data/faiss/langchain_index"
        )
    }


    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            config,
            file,
            indent=2
        )


    print()
    print("=" * 65)
    print("LANGCHAIN FAISS INDEX CREATED")
    print("=" * 65)

    print()
    print(
        "Index:"
    )

    print(
        INDEX_DIR / "index.faiss"
    )

    print(
        INDEX_DIR / "index.pkl"
    )

    print()
    print(
        "LangChain is now responsible for:"
    )

    print(
        "  Document creation"
    )

    print(
        "  FastEmbed embeddings"
    )

    print(
        "  FAISS vector-store creation"
    )

    print(
        "  Local vector-store persistence"
    )


if __name__ == "__main__":

    build_index()