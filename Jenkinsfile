pipeline {
    agent any

    triggers{
        githubPush()
    }

    stages {
        stage('Cleanup') {
            steps {
                script {
                    // Derruba containers em execução e remove imagens antigas
                    sh 'docker-compose down'
                    sh 'docker rmi -f docker-project || true'
                    sh 'docker rmi -f docker-project || true'
                }
            }
        }

        stage('Start Services') {
            steps {
                script {
                    // Inicia os containers com docker-compose
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executado com sucesso!'
        }
        failure {
            echo 'Pipeline falhou.'
        }
    }
}
