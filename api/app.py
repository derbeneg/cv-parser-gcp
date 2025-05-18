# api/app.py

from fastapi import FastAPI, UploadFile, File, HTTPException
import traceback
from parser import parse

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/parse")
async def parse_endpoint(cv: UploadFile = File(...)):
    try:
        cv_bytes = await cv.read()
        return parse(cv_bytes)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
