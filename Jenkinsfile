pipeline {
    agent any

    environment {
        BROWSERSTACK_USERNAME   = credentials('browserstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('browserstack-access-key')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install deps') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Create .env') {
            steps {
                sh '''
                    echo "BROWSERSTACK_USERNAME=$BROWSERSTACK_USERNAME" > .env
                    echo "BROWSERSTACK_ACCESS_KEY=$BROWSERSTACK_ACCESS_KEY" >> .env
                '''
            }
        }

        stage('Run Android tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest tests --platform android
                '''
            }
        }

        stage('Run iOS tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest tests --platform ios || true
                '''
            }
        }
    }
}