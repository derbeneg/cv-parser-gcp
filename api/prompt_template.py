PROMPT_TEMPLATE = """
Extract the following JSON schema from this CV text:
{"skills":[], "leadership_experience":[], "past_companies":[], 
 "roles_of_interest":[], "years_of_experience":[], "industries":[]}
Allowed skills: {skills}
Allowed roles: {roles}
Allowed industries: {industries}
Allowed leadership levels: {leadership}
Allowed experience buckets: {experience}

CV Text:
\"\"\"{text}\"\"\"
"""
