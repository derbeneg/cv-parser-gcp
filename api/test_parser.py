# api/test_parser.py

import json
import pytest
from api import parser

# A dummy response object to mimic genai_client.models.generate_content()
class DummyResponse:
    def __init__(self, text: str):
        self.text = text

@pytest.fixture(autouse=True)
def stub_gemini_and_pdf(monkeypatch):
    """
    1) Monkey-patch parser.extract_text so we don’t need a real PDF.
    2) Monkey-patch parser.genai_client.models.generate_content
       to return a fenced JSON blob every time.
    """
    # Stub out PDF text extraction
    monkeypatch.setattr(
        parser,
        "extract_text",
        lambda pdf_bytes_io: "this is dummy CV text"
    )

    # Stub out the GenAI call
    def fake_generate_content(model, contents):
        raw = (
            "```json\n"
            "{\"skills\": [\"Python\", \"Java\"], "
            "\"leadership_experience\": [], "
            "\"past_companies\": [], "
            "\"roles_of_interest\": [], "
            "\"years_of_experience\": [], "
            "\"industries\": []}"
            "\n```"
        )
        return DummyResponse(raw)

    monkeypatch.setattr(
        parser.genai_client.models,
        "generate_content",
        fake_generate_content
    )

    return monkeypatch

def test_clean_llm_json_strips_fences_and_labels():
    raw = "```json\n{\"foo\": 1}```"
    cleaned = parser.clean_llm_json(raw)
    assert cleaned == '{"foo": 1}'

def test_parse_with_gemini_returns_expected_dict():
    # With both extract_text and generate_content stubbed,
    # parse_with_gemini should return our dummy dict.
    result = parser.parse_with_gemini(b"not a real pdf")
    assert isinstance(result, dict)
    assert result == {
        "skills": ["Python", "Java"],
        "leadership_experience": [],
        "past_companies": [],
        "roles_of_interest": [],
        "years_of_experience": [],
        "industries": []
    }
