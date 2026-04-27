# ACEest Fitness & Gym - DevOps CI/CD Assignment

This project is a ready-to-submit DevOps CI/CD implementation for the ACEest Fitness & Gym assignment.

## Contents

- Flask application: `app/ACEest_Fitness.py`
- Unit tests: `tests/test_aceest_fitness.py`
- Jenkins pipeline: `Jenkinsfile`
- Dockerfile: `Dockerfile`
- SonarQube config: `sonar-project.properties`
- Kubernetes manifests: `k8s/`
- Report: `docs/ACEest_DevOps_Report.docx`

## Local Run

```bash
cd ACEest_DevOps_Assignment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
pip install -r app/requirements.txt
python app/ACEest_Fitness.py
```

Open: http://localhost:5000

## Run Tests

```bash
pytest tests --cov=app --cov-report=xml
```

## Docker Run

```bash
docker build -t aceest-fitness:v1 .
docker run -p 5000:5000 aceest-fitness:v1
```

## Minikube Deployment

```bash
minikube start
kubectl apply -f k8s/rolling-deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service aceest-fitness-service --url
```

## Docker Hub Push

Replace `YOUR_DOCKERHUB_USERNAME` in all files first.

```bash
docker tag aceest-fitness:v1 YOUR_DOCKERHUB_USERNAME/aceest-fitness:v1
docker push YOUR_DOCKERHUB_USERNAME/aceest-fitness:v1
```
