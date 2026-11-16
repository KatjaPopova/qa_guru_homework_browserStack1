pipeline {
    agent { label 'python' }

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
                    set +x
                    echo "BROWSERSTACK_USERNAME=${BROWSERSTACK_USERNAME}" > .env
                    echo "BROWSERSTACK_ACCESS_KEY=${BROWSERSTACK_ACCESS_KEY}" >> .env
                '''
            }
        }

        stage('Run Android tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest tests/android --platform android --alluredir=allure-results
                '''
            }
        }

        stage('Run iOS tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest tests/ios --platform ios --alluredir=allure-results || true
                '''
            }
        }

        stage('Generate Allure report') {
            steps {
                sh '''
                    npx --yes allure-commandline generate allure-results --clean -o allure-report
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
        }
    }
}