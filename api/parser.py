# api/parser.py

import os
import io
import csv
import json
import re
from pdfminer.high_level import extract_text
from api.prompt_template import PROMPT_TEMPLATE

# new Gen AI SDK imports
from google import genai

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [row[0] for row in csv.reader(f) if row]

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

ALLOWED_SKILLS      = load_csv(os.path.join(CONFIG_DIR, 'tech_skills.csv'))
ALLOWED_ROLES       = load_csv(os.path.join(CONFIG_DIR, 'roles.csv'))
ALLOWED_INDUSTRIES  = load_csv(os.path.join(CONFIG_DIR, 'industries.csv'))
ALLOWED_LEADERSHIP  = load_csv(os.path.join(CONFIG_DIR, 'leadership_experience.csv'))
ALLOWED_EXPERIENCE  = load_csv(os.path.join(CONFIG_DIR, 'work_experience.csv'))

# initialize a single GenAI client for Gemini on Vertex AI
genai_client = genai.Client(
    vertexai=True,
    project=os.getenv("GCP_PROJECT"),
    location=os.getenv("GCP_LOCATION", "us-central1")
)

def clean_llm_json(raw: str) -> str:
    s = raw.strip()
    # remove triple-backtick fences
    if s.startswith("```"):
        # strip any number of backticks at start/end
        s = re.sub(r"^```+(\w+)?", "", s)
        s = re.sub(r"```+$",     "", s)
    # if they prefixed with "json\n", drop that too
    s = re.sub(r"^json\s*\n", "", s, flags=re.IGNORECASE)
    return s.strip()

def parse_with_gemini(cv_bytes: bytes) -> dict:
    text = extract_text(io.BytesIO(cv_bytes))
    prompt = PROMPT_TEMPLATE.format(
        skills=ALLOWED_SKILLS,
        roles=ALLOWED_ROLES,
        industries=ALLOWED_INDUSTRIES,
        leadership=ALLOWED_LEADERSHIP,
        experience=ALLOWED_EXPERIENCE,
        text=text
    )
    response = genai_client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001"),
        contents=prompt
    )
    raw = response.text or ""
    cleaned = clean_llm_json(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(f"Couldn't parse JSON.\nRaw:\n{raw}\n\nCleaned:\n{cleaned}")

def parse_with_chatgpt(cv_bytes: bytes) -> dict:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    text = extract_text(io.BytesIO(cv_bytes))
    prompt = PROMPT_TEMPLATE.format(
        skills=ALLOWED_SKILLS,
        roles=ALLOWED_ROLES,
        industries=ALLOWED_INDUSTRIES,
        leadership=ALLOWED_LEADERSHIP,
        experience=ALLOWED_EXPERIENCE,
        text=text
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )
    try:
        return json.loads(resp.choices[0].message.content)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from ChatGPT: {resp.choices[0].message.content}")

def parse(cv_bytes: bytes) -> dict:
    mode = os.getenv("PARSER_MODE", "gemini").lower()
    if mode == "chatgpt":
        return parse_with_chatgpt(cv_bytes)
    return parse_with_gemini(cv_bytes)
