pipeline {
    agent any

    environment {
        // Variáveis de ambiente, como imagem Docker, etc
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'meu_app_image'
    }

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

        stage('Rodar Testes') {
            steps {
                script {
                    // Verificar se o container está em execução
                    echo 'Verificando se o container flask_app_container está em execução...'
                    sh 'docker ps -q --filter "name=flask_app_container" || (echo "flask_app_container não está em execução" && exit 1)'
                    
                    // Rodar testes após o start dos serviços
                    echo 'Rodando os testes...'
                    sh 'docker exec -T flask_app_container pytest tests/test_app.py'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build da imagem Docker (caso necessário)
                    echo 'Construindo a imagem Docker...'
                    sh 'docker-compose build'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy da aplicação (executar a imagem em modo detached)
                    echo 'Realizando o deploy...'
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executada com sucesso! Todos os serviços estão no ar.'
        }
        failure {
            echo 'Pipeline falhou. Verifique os logs para mais detalhes.'
            // Exibe logs do container em caso de falha
            sh 'docker logs flask_app_container'
        }
    }
}
