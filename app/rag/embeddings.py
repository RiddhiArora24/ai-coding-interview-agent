import os
from pathlib import Path

from langchain_community.embeddings import FastEmbedEmbeddings


MODEL_NAME = "BAAI/bge-small-en-v1.5"


def get_embeddings():

    cache_dir = os.getenv(
        "FASTEMBED_CACHE_DIR"
    )

    kwargs = {
        "model_name": MODEL_NAME,
        "doc_embed_type": "passage"
    }

    if cache_dir:

        Path(
            cache_dir
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        kwargs[
            "cache_dir"
        ] = cache_dir

    return FastEmbedEmbeddings(
        **kwargs
    )
