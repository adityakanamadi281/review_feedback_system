# CustomerPulse — Feedback System

A minimal feedback collection and analysis system with a Streamlit frontend, FastAPI backend, local LLM integration (via Ollama + `llama3.2`), and an SQLite database.

## Project structure

- `feedback_system/`
  - `app.py` — Streamlit frontend (user + admin dashboards)
  - `backend.py` — FastAPI backend providing `/submit` and `/admin`
  - `database.py` — SQLite helpers (DB at `feedback_system/data/feedback.db`)
  - `llm.py` — Local LLM integration (calls Ollama at `http://localhost:11434`)
  - `requirements.txt` — Python dependencies
  - `data/feedback.db` — SQLite database (created by the app)

## Prerequisites

- Python 3.11+ (project uses a virtual environment)
- Ollama running locally with model `llama3.2` available and the API listening on `http://localhost:11434`

## Quick start (Windows PowerShell)

From the project root (`c:\Users\adity\CustomerPulse`):

1. Create / activate virtual environment (if you don't have one):

```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r feedback_system/requirements.txt
```

3. Start the FastAPI backend (from project root):

```powershell
C:/Users/adity/CustomerPulse/.venv/Scripts/python.exe -m uvicorn feedback_system.backend:app --host 127.0.0.1 --port 8000
```

You should see startup logs; the backend will serve:
- `POST /submit` — accepts JSON `{ "rating": <int>, "review": "<text>" }`
- `GET /admin` — returns stored feedback rows

4. Start the Streamlit frontend (in a separate shell):

```powershell
C:/Users/adity/CustomerPulse/.venv/Scripts/streamlit run feedback_system/app.py
```

Open the UI at `http://localhost:8501`.

## API usage examples

- Submit a review (curl):

```bash
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{"rating":5, "review":"Great service!"}'
```

- Get all reviews (curl):

```bash
curl http://localhost:8000/admin
```

## Local LLM (Ollama + llama3.2)

This project expects a local Ollama service that exposes a JSON `POST /api/generate` endpoint. The `feedback_system/llm.py` file calls:

- `http://localhost:11434/api/generate` with `model: "llama3.2"`

Make sure Ollama is running and the `llama3.2` model is available. If your Ollama instance uses a different host/port or model name, update `feedback_system/llm.py` accordingly.

## Database

- SQLite DB file: `feedback_system/data/feedback.db`
- Schema (created automatically by `database.init_db()`):
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `rating` INTEGER
  - `review` TEXT
  - `ai_response` TEXT
  - `ai_summary` TEXT
  - `ai_action` TEXT

You can inspect records with the sqlite3 CLI or via Python:

```python
import sqlite3
conn = sqlite3.connect('feedback_system/data/feedback.db')
print(conn.execute('SELECT COUNT(*) FROM feedback').fetchone())
conn.close()
```

## Troubleshooting

- "Cannot connect to backend API":
  - Ensure the backend is running (uvicorn) and listening on `127.0.0.1:8000`.
  - Confirm `API_URL` in `feedback_system/app.py` is set to `http://localhost:8000`.

- LLM errors / timeouts:
  - Ensure Ollama is running and reachable at `http://localhost:11434`.
  - Increase timeout in `feedback_system/llm.py` `requests.post(..., timeout=60)` if needed.

- Import errors when starting `uvicorn feedback_system.backend:app`:
  - Verify `feedback_system/__init__.py` exists and imports are relative (e.g. `from .database import ...`).



