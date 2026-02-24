pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                bat 'pytest -q web_ui_framework --html=reports/html_reports/report.html --self-contained-html'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/html_reports/**', allowEmptyArchive: true
                }
            }
        }
    }
}
