# GitHub PR Analyzer

Lightweight FastAPI service that summarizes and analyzes GitHub pull requests using embeddings and an LLM.

**Key files**
- app/: application source
- requirements.txt: Python dependencies
- scripts/setup_venv.ps1: Windows venv + install script
- chroma_db/: persistent Chroma DB directory

## Requirements
- Python 3.10+ (recommended)
- Git
- Internet access for API calls and model endpoints

## Environment variables
Create a `.env` in the repository root with the following values:

```
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
OPENROUTER_API_KEY=your_openrouter_api_key
HF_TOKEN=your_huggingface_token
JWT_SECRET_KEY=your_long_jwt_secret_at_least_32_chars
JWT_ALGORITHM=HS256            # optional, default HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30 # optional, default 30
```

## Setup (Windows PowerShell)
From the repository root run:

```powershell
# create venv, activate and install deps
.\scripts\setup_venv.ps1
```

Then in any new PowerShell session activate the venv:

```powershell
& .\.venv\Scripts\Activate.ps1
```

## Setup (macOS / Linux)
Create and activate a venv, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the server
After activating the virtual environment and setting `.env`, start the FastAPI app:

```bash
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the API docs.

## Notes
- The app uses Chroma for vector storage and persists data to the `chroma_db/` folder.
- Embeddings use a Hugging Face endpoint (set `HF_TOKEN`).
- LLM calls go through OpenRouter (set `OPENROUTER_API_KEY`).
- Keep `JWT_SECRET_KEY` secure and long (>=32 chars).

## Troubleshooting
- If `app.config` raises a ValueError on startup, confirm the required env vars are present in `.env`.
- If embedding/LLM calls fail, confirm tokens and network access.

If you'd like, I can:
- pin dependency versions in `requirements.txt`,
- add a Unix `scripts/setup_venv.sh`, or
- create a small `.env.example` file.
