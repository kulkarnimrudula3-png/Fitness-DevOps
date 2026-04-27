# Step-by-Step: How to Run Everything on Laptop

## 1. Install Required Tools

Install these tools:
- Python 3.11+
- Git
- Docker Desktop
- Jenkins
- Java 17 for Jenkins/SonarQube
- SonarQube Community Edition
- Minikube
- kubectl

Check versions:
```bash
python --version
git --version
docker --version
java -version
kubectl version --client
minikube version
```

## 2. Run Flask App Locally

```bash
cd ACEest_DevOps_Assignment
python -m venv venv
venv\Scripts\activate
pip install -r app/requirements.txt
python app/ACEest_Fitness.py
```

Open:
```text
http://localhost:5000
http://localhost:5000/health
http://localhost:5000/members
http://localhost:5000/plans
```

## 3. Run Unit Tests

```bash
pytest tests --cov=app --cov-report=xml
```

Expected result: all tests should pass.

## 4. Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial ACEest Fitness DevOps assignment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aceest-fitness-devops.git
git push -u origin main
```

Create version tag:
```bash
git tag v1.0
git push origin v1.0
```

## 5. Build and Run Docker Image

```bash
docker build -t aceest-fitness:v1 .
docker run -p 5000:5000 aceest-fitness:v1
```

Open:
```text
http://localhost:5000
```

## 6. Push Docker Image to Docker Hub

```bash
docker login
docker tag aceest-fitness:v1 YOUR_DOCKERHUB_USERNAME/aceest-fitness:v1
docker tag aceest-fitness:v1 YOUR_DOCKERHUB_USERNAME/aceest-fitness:latest
docker push YOUR_DOCKERHUB_USERNAME/aceest-fitness:v1
docker push YOUR_DOCKERHUB_USERNAME/aceest-fitness:latest
```

Important: Replace `YOUR_DOCKERHUB_USERNAME` inside Kubernetes YAML and Jenkinsfile.

## 7. Run SonarQube Locally

Start SonarQube using Docker:
```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:community
```

Open:
```text
http://localhost:9000
```

Default login:
```text
username: admin
password: admin
```

Install scanner or configure scanner in Jenkins. Then run:
```bash
sonar-scanner
```

## 8. Deploy on Minikube / Kubernetes

Start Minikube:
```bash
minikube start
```

Apply deployment:
```bash
kubectl apply -f k8s/rolling-deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check pods:
```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

Get app URL:
```bash
minikube service aceest-fitness-service --url
```

## 9. Rolling Update

After building a new image version:
```bash
kubectl set image deployment/aceest-fitness-rolling aceest-fitness=YOUR_DOCKERHUB_USERNAME/aceest-fitness:v2
kubectl rollout status deployment/aceest-fitness-rolling
```

Rollback:
```bash
kubectl rollout undo deployment/aceest-fitness-rolling
```

## 10. Blue-Green Deployment

Deploy blue and green:
```bash
kubectl apply -f k8s/blue-deployment.yaml
kubectl apply -f k8s/green-deployment.yaml
kubectl apply -f k8s/blue-green-service.yaml
```

Initially service points to blue. To switch to green, edit `blue-green-service.yaml`:
```yaml
version: green
```

Then apply:
```bash
kubectl apply -f k8s/blue-green-service.yaml
```

Rollback: change selector back to blue.

## 11. Canary Release

Deploy stable version normally, then deploy canary:
```bash
kubectl apply -f k8s/rolling-deployment.yaml
kubectl apply -f k8s/canary-deployment.yaml
```

Only a small number of pods run the new version.

## 12. Shadow Deployment

```bash
kubectl apply -f k8s/shadow-deployment.yaml
```

In real production, traffic mirroring is configured using ingress or service mesh.

## 13. A/B Testing

```bash
kubectl apply -f k8s/ab-testing-v1.yaml
kubectl apply -f k8s/ab-testing-v2.yaml
```

Use ingress/controller rules to route users to version A or B.

## 14. Jenkins Setup

1. Open Jenkins: `http://localhost:8080`
2. Install plugins:
   - Git
   - Pipeline
   - Docker Pipeline
   - SonarQube Scanner
   - Kubernetes CLI
3. Add credentials:
   - Docker Hub credentials with ID: `dockerhub-credentials`
4. Configure SonarQube server name as: `SonarQubeServer`
5. Create Pipeline job.
6. Select Pipeline from SCM.
7. Add GitHub repository URL.
8. Set script path: `Jenkinsfile`.
9. Build now.

## 15. Screenshots to Add in Final Submission

Add screenshots of:
- GitHub repository commits
- Pytest successful output
- Jenkins successful pipeline
- Docker image in Docker Hub
- SonarQube dashboard
- Kubernetes pods and service
- Running application URL
