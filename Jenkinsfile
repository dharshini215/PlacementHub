pipeline {

    agent any

    stages {

        stage('Checkout Source') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/dharshini215/PlacementHub.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker-compose build'
            }
        }

        stage('Deploy Container') {
            steps {
                bat 'docker-compose down'
                bat 'docker-compose up -d'
            }
        }

    }

    post {

        success {
            echo 'PlacementHub deployed successfully!'
        }

        failure {
            echo 'Deployment failed!'
        }

    }

}