import uvicorn
from src.service import app

if __name__ == "__main__":
    # For local development: hot reload, 0.0.0.0 for Docker compatibility
    uvicorn.run("src.service:app", host="0.0.0.0", port=8000, reload=True)
