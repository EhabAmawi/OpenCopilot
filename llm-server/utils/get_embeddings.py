from langchain.embeddings.openai import OpenAIEmbeddings
from enums.embedding_provider import EmbeddingProvider
import os
from dotenv import load_dotenv
from langchain.embeddings.base import Embeddings
from langchain.embeddings import LlamaCppEmbeddings

load_dotenv()


def get_embedding_provider() -> str:
    """Gets the chosen embedding provider from environment variables."""
    return os.environ.get("EMBEDDING_PROVIDER") or "openai"


def get_azure_embedding() -> Embeddings:
    """Gets embeddings using the Azure embedding provider."""
    deployment = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL_NAME")
    openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    client = os.environ.get("AZURE_OPENAI_API_TYPE")
    openai_api_base = os.environ["AZURE_OPENAI_API_BASE"]
    openai_api_version = os.environ["AZURE_OPENAI_API_VERSION"]

    return OpenAIEmbeddings(
        openai_api_key=openai_api_key,
        deployment=deployment,
        client=client,
        chunk_size=8,
        openai_api_base=openai_api_base,
        openai_api_version=openai_api_version,
    )


def get_openai_embedding() -> Embeddings:
    """Gets embeddings using the OpenAI embedding provider."""
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    return OpenAIEmbeddings(openai_api_key=openai_api_key, chunk_size=1)


def get_llama2_embedding() -> Embeddings:
    """Gets embeddings using the llama2 embedding provider."""
    return LlamaCppEmbeddings(model_path="llama-2-7b-chat.ggmlv3.q4_K_M.bin")


def choose_embedding_provider() -> Embeddings:
    """Chooses and returns the appropriate embedding provider instance."""
    embedding_provider = get_embedding_provider()

    if embedding_provider == EmbeddingProvider.azure.value:
        return get_azure_embedding()

    elif embedding_provider == EmbeddingProvider.OPENAI.value:
        return get_openai_embedding()

    elif embedding_provider == EmbeddingProvider.llama2.value:
        return get_llama2_embedding()

    else:
        # instead of throwing error, we can probably use a default like spaCy embeddings
        available_providers = ", ".join(
            [service.value for service in EmbeddingProvider]
        )
        raise ValueError(
            f"Embedding service '{embedding_provider}' is not currently available. "
            f"Available services: {available_providers}"
        )


# Main function to get embeddings
def get_embeddings() -> Embeddings:
    """Gets embeddings using the chosen embedding provider."""
    return choose_embedding_provider()
