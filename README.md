# cv-parser-gcp
Cloud-native CV-parsing pipeline on GCP (GKE, VM, Cloud Functions, Pub/Sub) with Locust performance tests

# CV-Parser-GCP

A cloud-native CV-parsing pipeline on Google Cloud Platform (GCP), featuring:
- **Containerized API** (FastAPI + Docker)
- **Configurable parser adapter** (open-source or LLM)
- **Event-driven architecture** (Pub/Sub → Cloud Functions + optional VM worker)
- **Performance testing** with Locust
- **Infrastructure as Code** (Terraform + Kubernetes manifests)

---

## Folder Structure

cv-parser-gcp/
├── api/ # FastAPI service & Dockerfile
│ ├── app.py
│ ├── parser.py # parser adapter stubs
│ ├── Dockerfile
│ └── requirements.txt
├── locust/ # load-test scripts
│ └── locustfile.py
├── terraform/ # Terraform modules & k8s YAMLs
├── docs/ # architecture diagrams & cost breakdown
└── README.md


---

## Prerequisites

- Docker Desktop (or Docker Engine) installed and running  
- (Optional) Python 3.10+ & `pip` for local venv testing  

---

## Quickstart (Local Docker)

1. **Build** the API image  
   ```bash
   cd api
   docker build -t cv-parser-api:latest .

2. **Run** the Conatiner

    docker run -it --rm -p 8080:8080 cv-parser-api:latest

3. **Verify** service health

    curl http://localhost:8080/health
    # Returns: {"status":"ok"}

4. **Test** parsing stub

    curl -F "cv=@samples/john_doe.pdf" http://localhost:8080/parse
    # Returns stubbed JSON with empty lists
