import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT)
)

from app.rag.retriever import QuestionRetriever


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--query",
        default="array hashing interview problem"
    )

    parser.add_argument(
        "--company",
        default=None
    )

    parser.add_argument(
        "--difficulty",
        default=None
    )

    parser.add_argument(
        "--k",
        type=int,
        default=4
    )

    args = parser.parse_args()

    retriever = QuestionRetriever()

    results = retriever.search(
        query=args.query,
        company=args.company,
        difficulty=args.difficulty,
        k=args.k
    )

    print()
    print("=" * 70)
    print("RAG RETRIEVAL RESULTS")
    print("=" * 70)

    print(f"Query      : {args.query}")
    print(f"Company    : {args.company or 'Any'}")
    print(f"Difficulty : {args.difficulty or 'Any'}")
    print()

    if not results:
        print("No matching questions found.")
        return

    for i, q in enumerate(results, 1):

        print("-" * 70)

        print(
            f"{i}. {q['title']}"
        )

        print(
            f"ID         : {q['id']}"
        )

        print(
            f"Company    : {q['company']}"
        )

        print(
            f"Difficulty : {q['difficulty']}"
        )

        print(
            f"Topics     : {', '.join(q['topics'])}"
        )

        print(
            f"Similarity : {q['score']}"
        )

    print("-" * 70)


if __name__ == "__main__":
    main()
