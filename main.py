import os
import time
import uuid
from typing import List

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

# Keep these defaults aligned with the assignment screenshot. Set environment
# variables in your hosting dashboard if your assigned values change.
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "https://dash-2ql9iq.example.com").strip()
EXAM_EMAIL = os.getenv("EXAM_EMAIL", "22f2000074@ds.study.iitm.ac.in").strip()

app = FastAPI(title="Exam Statistics API", docs_url="/docs", redoc_url=None)

# Exact origin only. Never use '*' for this assignment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"] ,
    max_age=600,
)


@app.middleware("http")
async def add_request_metadata(request: Request, call_next):
    """Attach a unique request ID and handler duration to every response."""
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        # Still let FastAPI/Starlette handle the error normally where possible;
        # this branch ensures metadata is added to a fallback 500 response.
        response = Response(content='{"detail":"Internal Server Error"}', status_code=500,
                            media_type="application/json")
    elapsed = max(time.perf_counter() - start, 0.0)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response


@app.get("/stats")
def stats(values: str = Query(..., description="Comma-separated integers")):
    raw_parts = values.split(",")
    if not raw_parts or any(not part.strip() for part in raw_parts):
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")

    try:
        numbers: List[int] = [int(part.strip()) for part in raw_parts]
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")

    if not numbers:
        raise HTTPException(status_code=400, detail="at least one integer is required")

    return {
        "email": EXAM_EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
    }


@app.get("/")
def health():
    return {"status": "ok", "service": "exam-statistics-api"}
