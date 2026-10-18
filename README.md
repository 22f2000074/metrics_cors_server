# Exam Statistics API with strict CORS

This FastAPI service implements `GET /stats?values=1,2,3`, calculates count/sum/min/max/mean for each fresh request, returns the configured exam email, and adds `X-Request-ID` plus `X-Process-Time` to every response.

## Assigned values

- Allowed CORS origin: `https://dash-2ql9iq.example.com`
- Exam email default: `22f2000074@ds.study.iitm.ac.in`

**Confirm the EXAM_EMAIL value matches the exact email address you use to log in to the grading site.** If it differs, change the `EXAM_EMAIL` environment variable in Render before deploying.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Test stats:

```bash
curl -i 'http://127.0.0.1:8000/stats?values=1,2,3,4'
```

Allowed-origin preflight (should return 200 and Access-Control-Allow-Origin with the assigned origin):

```bash
curl -i -X OPTIONS 'http://127.0.0.1:8000/stats' \
  -H 'Origin: https://dash-2ql9iq.example.com' \
  -H 'Access-Control-Request-Method: GET' \
  -H 'Access-Control-Request-Headers: content-type'
```

Unapproved-origin preflight (must not return Access-Control-Allow-Origin):

```bash
curl -i -X OPTIONS 'http://127.0.0.1:8000/stats' \
  -H 'Origin: https://evil.example' \
  -H 'Access-Control-Request-Method: GET'
```

## Deploy to Render

1. Create a GitHub repository and upload `main.py`, `requirements.txt`, `render.yaml`, and `.gitignore`.
2. In Render, choose **New → Blueprint** and connect the repository (or create a Web Service manually).
3. Use build command `pip install -r requirements.txt` and start command `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. Confirm environment variables `ALLOWED_ORIGIN` and `EXAM_EMAIL`. The latter must exactly match your logged-in exam email.
5. Wait until the service is Live.
6. Submit the **base URL** such as `https://your-service.onrender.com` (without `/stats`), as requested by the page.

The CORS middleware uses an exact allowlist (no wildcard). Allowed-origin OPTIONS requests are accepted; disallowed origins do not receive an `Access-Control-Allow-Origin` response header.
