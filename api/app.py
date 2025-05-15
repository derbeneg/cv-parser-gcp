# api/app.py
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/parse")
async def parse(cv: UploadFile = File(...)):
    # Stub parser: return empty lists
    return {
        "skills": [],
        "leadership_experience": [],
        "past_companies": [],
        "roles_of_interest": []
    }
