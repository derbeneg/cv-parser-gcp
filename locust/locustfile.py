# locust/locustfile.py

import os
from locust import HttpUser, TaskSet, task, between

class CVParseTasks(TaskSet):
    @task
    def parse_cv(self):
        # Compute the absolute path to the sample PDF
        project_root = os.path.dirname(os.path.dirname(__file__))
        sample_pdf = os.path.join(project_root, "api", "samples", "cv_bene.pdf")

        with open(sample_pdf, "rb") as pdf_file:
            files = {
                "cv": ("cv_bene.pdf", pdf_file, "application/pdf")
            }
            self.client.post("/parse", files=files, name="/parse")

class CVUser(HttpUser):
    tasks = [CVParseTasks]
    wait_time = between(1, 3)
    # host can be overridden on the command line with --host
    # host = "http://localhost:8080"
