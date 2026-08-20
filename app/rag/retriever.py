import json
from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.rag.embeddings import (
    get_embeddings
)


ROOT = Path(__file__).resolve().parents[2]

INDEX_DIR = (
    ROOT
    / "data"
    / "faiss"
    / "langchain_index"
)

DATA_FILE = (
    ROOT
    / "data"
    / "questions.json"
)


class QuestionRetriever:
    """
    Semantic question retrieval implemented with
    LangChain + FAISS.
    """

    def __init__(self):

        if not INDEX_DIR.exists():

            raise FileNotFoundError(
                "LangChain FAISS index not found. "
                "Run app/rag/build_index.py first."
            )

        self.embeddings = (
            get_embeddings()
        )

        # index.pkl is created by our own application.
        self.vector_store = (
            FAISS.load_local(
                str(INDEX_DIR),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        )

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            self.questions = (
                json.load(file)
            )


    def search(
        self,
        query,
        company=None,
        difficulty=None,
        k=4
    ):

        filters = {}

        if company:

            filters[
                "company"
            ] = company

        if difficulty:

            filters[
                "difficulty"
            ] = difficulty


        results = (
            self.vector_store
            .similarity_search_with_score(
                query,
                k=k,
                filter=(
                    filters
                    if filters
                    else None
                ),
                fetch_k=max(
                    60,
                    k
                )
            )
        )


        output = []

        for document, distance in results:

            # LangChain FAISS returns a distance score.
            # Convert it into an easy-to-read monotonic
            # similarity-like value for our UI/tests.
            similarity = (
                1.0
                /
                (
                    1.0
                    + max(
                        0.0,
                        float(distance)
                    )
                )
            )

            output.append({
                "id": document.metadata[
                    "question_id"
                ],
                "title": document.metadata[
                    "title"
                ],
                "company": document.metadata[
                    "company"
                ],
                "difficulty": document.metadata[
                    "difficulty"
                ],
                "topics": document.metadata[
                    "topics"
                ],
                "text": document.page_content,
                "score": round(
                    similarity,
                    4
                )
            })


        return output


    def as_retriever(
        self,
        k=4
    ):
        """
        Exposes the standard LangChain Retriever interface.
        """

        return (
            self.vector_store
            .as_retriever(
                search_kwargs={
                    "k": k
                }
            )
        )