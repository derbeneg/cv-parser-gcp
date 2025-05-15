# api/parser.py

import os
import csv
import io
import json
from typing import List, Dict
from pdfminer.high_level import extract_text
from prompt_template import PROMPT_TEMPLATE

# ─── Load allowed values from CSVs ─────────────────────────────────────────────

def load_csv(path: str) -> List[str]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        return [row[0].strip() for row in reader if row and row[0].strip()]

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config'))
ALLOWED_ROLES      = load_csv(os.path.join(BASE, 'roles.csv'))
ALLOWED_INDUSTRIES = load_csv(os.path.join(BASE, 'industries.csv'))
ALLOWED_LEADERSHIP = load_csv(os.path.join(BASE, 'leadership_experience.csv'))
ALLOWED_EXPERIENCE = load_csv(os.path.join(BASE, 'work_experience.csv'))
ALLOWED_SKILLS     = load_csv(os.path.join(BASE, 'tech_skills.csv'))

# ─── Gemini (Vertex AI) adapter ───────────────────────────────────────────────

def parse_with_gemini(cv_bytes: bytes) -> Dict[str, List[str]]:
    from google.cloud import aiplatform
    project  = os.getenv("GCP_PROJECT")
    location = os.getenv("GCP_LOCATION", "us-central1")
    model    = os.getenv("GEMINI_MODEL", "chat-bison-001")
    client   = aiplatform.TextGenerationServiceClient()
    name     = client.model_path(project, location, model)

    text = extract_text(io.BytesIO(cv_bytes))
    prompt = PROMPT_TEMPLATE.format(
        skills=ALLOWED_SKILLS,
        roles=ALLOWED_ROLES,
        industries=ALLOWED_INDUSTRIES,
        leadership=ALLOWED_LEADERSHIP,
        experience=ALLOWED_EXPERIENCE,
        text=text
    )
    response = client.generate_text(name=name, prompt=prompt, temperature=0.0)
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from Gemini: {response.text}")

# ─── ChatGPT (OpenAI) adapter ─────────────────────────────────────────────────

def parse_with_chatgpt(cv_bytes: bytes) -> Dict[str, List[str]]:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

    text = extract_text(io.BytesIO(cv_bytes))
    messages = [
        {"role": "system", "content": "You extract CV info into a strict JSON schema."},
        {"role": "user",   "content": text}
    ]
    function_def = {
        "name": "extract_cv",
        "description": "Extract CV into JSON schema",
        "parameters": {
            "type": "object",
            "properties": {
                "skills":               {"type": "array", "items": {"type": "string"}},
                "leadership_experience":{"type": "array", "items": {"type": "string"}},
                "past_companies":       {"type": "array", "items": {"type": "string"}},
                "roles_of_interest":    {"type": "array", "items": {"type": "string"}},
                "years_of_experience":  {"type": "array", "items": {"type": "string"}},
                "industries":           {"type": "array", "items": {"type": "string"}}
            },
            "required": [
                "skills", "leadership_experience", "past_companies",
                "roles_of_interest", "years_of_experience", "industries"
            ]
        }
    }
    resp = openai.ChatCompletion.create(
        model=os.getenv("CHATGPT_MODEL", "gpt-4o"),
        messages=messages,
        temperature=0.0,
        functions=[function_def],
        function_call={"name": "extract_cv"}
    )
    message = resp.choices[0].message
    if message.get("function_call"):
        args_str = message.function_call.arguments
        try:
            return json.loads(args_str)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON from ChatGPT: {args_str}")
    else:
        raise ValueError("No function call returned by ChatGPT")

# ─── Dispatcher ───────────────────────────────────────────────────────────────

def parse(cv_bytes: bytes) -> Dict[str, List[str]]:
    mode = os.getenv("PARSER_MODE", "gemini").lower()
    if mode == "chatgpt":
        return parse_with_chatgpt(cv_bytes)
    return parse_with_gemini(cv_bytes)
