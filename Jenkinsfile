pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "YOUR_DOCKERHUB_USERNAME/aceest-fitness"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python3 -m pip install --upgrade pip'
                bat 'pip install -r app/requirements.txt'
            }
        }

        stage('Run Pytest') {
            steps {
                bat 'pytest tests --cov=app --cov-report=xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Configure SonarQube server in Jenkins as SonarQubeServer'
                withSonarQubeEnv('SonarQubeServer') {
                    bat 'sonar-scanner'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t $DOCKER_IMAGE:$IMAGE_TAG -t $DOCKER_IMAGE:latest .'
            }
        }

        stage('push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    bat 'docker push $DOCKER_IMAGE:$IMAGE_TAG'
                    bat 'docker push $DOCKER_IMAGE:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f k8s/rolling-deployment.yaml'
                bat 'kubectl apply -f k8s/service.yaml'
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check tests, SonarQube quality gate, Docker build, or Kubernetes deployment.'
        }
    }
}
