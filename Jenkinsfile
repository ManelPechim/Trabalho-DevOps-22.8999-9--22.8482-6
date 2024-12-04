pipeline {
    agent any

    environment {
        // Definindo variáveis para os containers e repositório
        REPO_URL = 'https://github.com/ManelPechim/Trabalho-DevOps-22.8999-9--22.8482-6.git'
        BRANCH = 'main'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Baixando código do repositório Git...'
                    // Clonando o repositório Git
                    git branch: "${BRANCH}", url: "${REPO_URL}"
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    echo 'Realizando limpeza de containers e imagens antigas...'
                    // Derruba containers em execução e remove imagens antigas
                    sh 'docker-compose down --remove-orphans'
                    sh '''
                        docker images -q | xargs -r docker rmi -f || true
                    ''' // Remove imagens não usadas
                }
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    echo 'Realizando o build da aplicação e deploy...'
                    // Inicia os containers usando o arquivo docker-compose.yml
                    sh 'docker-compose up -d --build'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Rodando os testes dentro do container Flask...'
                    // Executando os testes dentro do container
                    sh "docker exec flask_app_container pytest /app/test_app.py -s"
                }
            }
        }

        stage('Monitor') {
            steps {
                script {
                    echo 'Verificando o estado dos containers...'
                    // Verificando os containers em execução após o deploy
                    sh 'docker ps'
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
