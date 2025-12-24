import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

LOG_FILE = "data/logs/history.csv"
APP_LOG_FILE = "data/logs/app.log"

def setup_logging():
    """Sets up logging for the application."""
    os.makedirs("data/logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(APP_LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True # Ensures handlers are not duplicated on re-runs in environments like Streamlit
    )
    # Suppress verbose logging from libraries like `sentence_transformers`
    logging.getLogger("sentence_transformers.SentenceTransformer").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("faiss.loader").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)

def save_query_log(query: str, answer: str, confidence: str, status: str):
    """Saves the query, answer, confidence, and timestamp to a CSV log file."""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "query": query,
        "answer": answer,
        "confidence": confidence,
        "status": status,  # e.g., '解決済み' (Resolved), '要改善' (Needs Improvement)
    }

    df = pd.DataFrame([log_entry])

    if not os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, index=False, encoding='utf-8-sig')
    else:
        df.to_csv(LOG_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
    logging.info(f"Query log saved to {LOG_FILE}")

def get_openai_api_key():
    """Retrieves the OpenAI API key from environment variables."""
    return os.getenv("OPENAI_API_KEY")
