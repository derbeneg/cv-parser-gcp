# locust/locustfile.py
import os
import json

from locust import HttpUser, TaskSet, task, between

SCHEMA_KEYS = [
    "skills",
    "leadership_experience",
    "past_companies",
    "roles_of_interest",
    "years_of_experience",
    "industries",
]

class CVParseTasks(TaskSet):
    @task
    def parse_cv(self):
        # locate sample PDF
        project_root = os.path.dirname(os.path.dirname(__file__))
        sample_pdf = os.path.join(project_root, "api", "samples", "cv_bene.pdf")

        with open(sample_pdf, "rb") as pdf_file:
            files = {"cv": ("cv_bene.pdf", pdf_file, "application/pdf")}
            with self.client.post(
                "/parse",
                files=files,
                name="/parse",
                catch_response=True,
                timeout=60,
            ) as response:

                # 1) status code
                if response.status_code != 200 and response.status_code != 0:
                    response.failure(f"Bad status: {response.status_code}")
                    return

                # 2) valid JSON?
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    response.failure("Invalid JSON")
                    return

                # 3) schema validation
                for key in SCHEMA_KEYS:
                    if key not in data:
                        response.failure(f"Missing key `{key}`")
                        return
                    if not isinstance(data[key], list):
                        response.failure(f"`{key}` not a list")
                        return

                # if we get here, it’s all good
                response.success()

class CVUser(HttpUser):
    tasks = [CVParseTasks]
    wait_time = between(1, 3)
    # host is set via --host on the CLI
