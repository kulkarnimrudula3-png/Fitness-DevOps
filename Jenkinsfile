pipeline {
    agent any

    environment {
         PYTHON_EXE = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        DOCKER_IMAGE = "kulkarnimrudula3/aceest-fitness"
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
                bat '"%PYTHON_EXE%" -m pip install --upgrade pip'
                bat '"%PYTHON_EXE%" -m pip install -r requirements.txt'
            }
        }

        stage('Run Pytest') {
            steps {
               bat '"%PYTHON_EXE%" -m pytest'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis'
                withSonarQubeEnv('SonarQubeServer') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        bat """
                        "${scannerHome}\\bin\\sonar-scanner" ^
                        -Dsonar.projectKey=fitness-app ^
                        -Dsonar.sources=. ^
                        -Dsonar.host.url=http://localhost:9000 ^
                        -Dsonar.login=%SONAR_AUTH_TOKEN%
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %DOCKER_IMAGE%:%IMAGE_TAG% -t %DOCKER_IMAGE%:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat "echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin"
                    bat "docker push %DOCKER_IMAGE%:%IMAGE_TAG%"
                    bat "docker push %DOCKER_IMAGE%:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat "kubectl apply -f k8s/rolling-deployment.yaml"
                bat "kubectl apply -f k8s/service.yaml"
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
