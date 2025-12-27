import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

# Configuration
DATA_DIR = "data/source_docs"
VECTOR_STORE_DIR = "data/vector_store"

# Initialize OpenAI LLM
llm = OpenAI(model="gpt-4o", temperature=0.0)

def initialize_rag_engine():
    """Initializes the RAG engine by loading documents and creating/loading the ChromaDB index."""
    # Create Chroma client
    db = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
    chroma_collection = db.get_or_create_collection("smart_support_ops")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Initialize embedding model
    # Note: HuggingFaceEmbedding will download the model the first time it's used.
    # Using a local cache folder to avoid path length issues and corruption on Windows
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
        cache_folder="./data/model_cache"
    )

    # Check if index already exists to avoid re-indexing on every run
    if len(chroma_collection.get()['ids']) == 0:
        logger.info("Creating new index...")
        # Load documents
        documents = SimpleDirectoryReader(DATA_DIR).load_data()

        # Create index
        index = VectorStoreIndex.from_documents(
            documents,
            vector_store=vector_store,
            embed_model=embed_model,
        )
    else:
        logger.info("Loading existing index...")
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=embed_model,
        )

    # Configure query engine
    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=3,
    )

    return query_engine

def query_rag_engine(query_engine, query: str):
    """Queries the RAG engine and returns the response, source nodes, and a confidence score."""
    response = query_engine.query(query)

    # Extract information
    answer = response.response
    source_nodes = response.source_nodes

    # Calculate a simple confidence score based on retrieval similarity scores
    # This is a basic implementation; more sophisticated scoring might be needed
    if source_nodes:
        # LlamaIndex scores are usually 0-1, higher is better.
        # Let's just take the score of the top node for simplicity as a confidence measure.
        # For more complex scenarios, you might average or use a weighted sum.
        top_score = source_nodes[0].score if source_nodes[0].score is not None else 0.0

        if top_score > 0.8:
            confidence = "高" # High
        elif top_score > 0.6:
            confidence = "中" # Medium
        else:
            confidence = "低" # Low
        confidence_percentage = f"{top_score * 100:.0f}%"
    else:
        confidence = "低" # Low (no source found)
        confidence_percentage = "0%"

    return answer, source_nodes, confidence, confidence_percentage
