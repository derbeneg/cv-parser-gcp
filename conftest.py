# conftest.py

import os, pathlib

# point ADC to your service-account JSON
# this is needed for test_parser.py (pytests) to work (able to access Vertex AI via gcp authentication) - 
# --> loads the service account key to ADC
os.environ.setdefault(
    "GOOGLE_APPLICATION_CREDENTIALS",
    str(pathlib.Path(__file__).parent / "secrets" / "vertex-sa.json")
)

# if you need a default project
os.environ.setdefault("GCP_PROJECT", "cv-parser-460110")
