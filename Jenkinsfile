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
stage('Debug Branch') {
    steps {
        bat '''
        echo ==========================
        echo BRANCH_NAME=%BRANCH_NAME%
        echo GIT_BRANCH=%GIT_BRANCH%
        echo GIT_LOCAL_BRANCH=%GIT_LOCAL_BRANCH%
        echo ==========================
        git rev-parse --abbrev-ref HEAD
        git branch
        '''
    }
}

        stage('Merge staging into develop') {
            when {
                branch 'staging'
            }

            steps {
                bat '''
                git config user.name "Jenkins CI"
                git config user.email "jenkins@local"

                git fetch origin

                git checkout develop
                git pull origin develop

                git merge origin/staging --no-ff -m "Auto merge staging into develop"

                git push origin develop
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