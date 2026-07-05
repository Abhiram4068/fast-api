pipeline {
    agent any

    environment {
        DATABASE_URL = 'postgresql://postgres:password1234@localhost:5432/fastapi_db_test'
        SECRET_KEY = 'test-secret-key-not-for-production'
        ALGORITHM = 'HS256'
        ACCESS_TOKEN_EXPIRE_MINUTES = '30'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat 'python -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                venv\\Scripts\\python -m pip install --upgrade pip
                venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                if not exist reports mkdir reports
                venv\\Scripts\\pytest -v --junitxml=reports\\test-results.xml
                '''
            }
        }
    }

    post {
        always {
            junit 'reports/test-results.xml'
        }
    }
}