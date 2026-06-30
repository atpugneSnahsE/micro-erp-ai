# Setup

```bash
git clone <repo>
cd micro-erp-ai

python3.11 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```