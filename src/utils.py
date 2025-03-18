import os

def ensure_directories():
    """Ensures required directories exist."""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

ensure_directories()
