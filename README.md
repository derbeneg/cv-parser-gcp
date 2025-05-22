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



------------------------------------

**1. Local deployment and smoke test**

# (a) Spin up your FastAPI service in Docker
make up
# → this runs docker compose up api, mounting your secrets and exposing :8080

# (b) Verify parsing works locally
curl -F "cv=@api/samples/cv_bene.pdf" http://localhost:8080/parse

# (c) (Optional) run your Locust spike locally
locust -f locust/locustfile.py --headless -u 10 -r 2 --run-time 1m --host http://localhost:8080

# (d) When you’re done hacking locally:
make down


**2. Cloud deployment & smoke-test**

# 1) Point Terraform at your service‐account
cd <project-root>
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/secrets/vertex-sa.json"

# 2) Provision (or re‐provision) your infra (GKE, SQL, Pub/Sub, VM, Function)
cd terraform
terraform init
terraform apply -auto-approve

# 3) Configure kubectl for your new GKE cluster
gcloud container clusters get-credentials cv-parser-gke-cluster \
  --region us-central1 \
  --project=cv-parser-460110
kubectl get nodes    # confirm Ready

# 4) Build & push your API Docker image
cd .. to root!
gcloud auth configure-docker
docker build -t cv-parser-api:dev ./api
docker tag cv-parser-api:dev gcr.io/cv-parser-460110/cv-parser-api:latest
docker push gcr.io/cv-parser-460110/cv-parser-api:latest

# 5) Build & push your VM worker Docker image
docker build -t cv-parser-worker:dev ./api/worker
docker tag cv-parser-worker:dev gcr.io/cv-parser-460110/cv-parser-worker:latest
docker push gcr.io/cv-parser-460110/cv-parser-worker:latest

# 6) Deploy your k8s manifests
cd /k8s
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f horizontalpodautoscaler.yaml

# 7) Wait for a public IP
kubectl get svc cv-parser-svc --watch

# 8) Smoke‐test your cloud endpoint
cd ..
curl -F "cv=@api/samples/cv_bene.pdf" http://<EXTERNAL_IP>/parse

# 9) Verify Cloud Function subscription
gcloud pubsub topics publish cv-parse-topic --message='{"test":"msg"}'
gcloud functions logs read cv-parse-logger --limit=10

# 10) Verify your VM worker
gcloud compute ssh cv-parser-worker --zone us-central1-a
**# WAIT a bit! takes some time**
docker ps
docker logs <worker_container_id>    # should show “VM got message: {…}”

# 11) (Optional) verify other resources
gcloud sql instances describe cv-parser-db
gcloud pubsub topics list
gcloud pubsub subscriptions list

# 12) Running my locust tests (from root)
bash -x docs/locust/gcp/run_gcp_tests.sh

# When you’re done & to avoid cost:
cd terraform
terraform destroy -auto-approve



**Destroy everything**

# Tear down everything
cd terraform
terraform destroy -auto-approve
