pipeline {
    agent any

    stages {
        stage('Cleanup') {
            steps {
                script {
                    // Derruba containers em execução e remove imagens antigas
                    echo 'Realizando limpeza de containers e imagens antigas...'
                    sh 'docker-compose down --remove-orphans' // Remove containers antigos
                    sh '''
                        docker images -q | xargs -r docker rmi -f || true
                    ''' // Remove imagens não usadas
                }
            }
        }

        stage('Start Services') {
            steps {
                script {
                    // Inicia os containers usando o arquivo docker-compose.yml
                    echo 'Iniciando os containers...'
                    sh 'docker-compose up -d --build'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executado com sucesso! Todos os serviços estão no ar.'
        }
        failure {
            echo 'Pipeline falhou. Verifique os logs para mais detalhes.'
        }
    }
}
