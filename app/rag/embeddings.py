from langchain_community.embeddings import FastEmbedEmbeddings


MODEL_NAME = "BAAI/bge-small-en-v1.5"


def get_embeddings():

    return FastEmbedEmbeddings(
        model_name=MODEL_NAME,
        doc_embed_type="passage"
    )