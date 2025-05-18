# api/prompt_template.py

# Template for LLM prompt; literal JSON braces escaped via double {{ }}
PROMPT_TEMPLATE = '''
Extract the following JSON schema from this CV text:
{{"skills":[], "leadership_experience":[], "past_companies":[],
  "roles_of_interest":[], "years_of_experience":[], "industries":[]}}
Allowed skills: {skills}
Allowed roles: {roles}
Allowed industries: {industries}
Allowed leadership levels: {leadership}
Allowed experience buckets: {experience}

CV Text:
\"\"\"{text}\"\"\"

**IMPORTANT:** output _only_ the JSON object, nothing else—no code fences, no markdown, no commentary.
'''
