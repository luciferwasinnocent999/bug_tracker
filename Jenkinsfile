pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/your/repo.git'
            }
        }

        stage('Build & Run') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d --build'
            }
        }
    }
}
