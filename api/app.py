# api/app.py

import os
from fastapi import FastAPI, UploadFile, File
from parser import parse   # our adapter dispatcher

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/parse")
async def parse_endpoint(cv: UploadFile = File(...)):
    cv_bytes = await cv.read()
    result = parse(cv_bytes)
    return result
