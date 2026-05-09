from fastapi import FastAPI

app = FastAPI()

@app.get("/api/inquiries/summary")
def get_summary():
    return {
        "total": 120,
        "open": 45,
        "closed": 70,
        "pending": 5,
        "categories": {"billing": 30, "technical": 50, "general": 40},
        "last_updated": "2026-05-09T00:00:00Z",
    }
