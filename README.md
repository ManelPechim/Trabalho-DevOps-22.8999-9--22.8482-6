# Trabalho de Disciplina - DevOps: Criação de Ambiente Monitorado com Pipeline CI/CD

## Membros

- **Walter Yoshio Gmack Ussuda** ; RA: 22.8482-6  
- **Emanuel Ferreira Pechim dos Santos** ; RA: 22.8999-9  
- **Marcella Eduarda Queiroz** ; RA: 22.7073-4  

## Descrição

Este trabalho configura um ambiente DevOps com **CI/CD**, utilizando **Jenkins**, **Docker**, **Prometheus** e **Grafana**. A aplicação web em **Flask** é integrada ao banco de dados **MariaDB**. A pipeline automatiza testes, build e deploy, e o monitoramento é feito com Prometheus e Grafana.

## Tecnologias

- **Jenkins**: Pipeline CI/CD
- **Docker**: Containerização
- **Flask**: Aplicação Web
- **MariaDB**: Banco de Dados
- **Prometheus**: Monitoramento
- **Grafana**: Dashboards

## Estrutura do Repositório

- `Dockerfile`: Imagem da aplicação.
- `docker-compose.yml`: Orquestração de containers.
- `Jenkinsfile`: Definição da pipeline.
- `prometheus.yml`: Configuração do Prometheus.
- `grafana/`: Dashboards e data sources.
- `app/`: Código da aplicação.
- `tests/`: Testes unitários.

## Como Rodar

1. Clone o repositório:
   ```bash
   git clone git@github.com:ManelPechim/Trabalho-DevOps-22.8999-9--22.8482-6.git
   cd Trabalho-DevOps-22.8999-9--22.8482-6

2. Execute o Docker Compose para subir os containers:
    ```bash
    docker-compose up -d --build

3. Configure o Jenkins:
    - Acesse o Jenkins em `http://localhost:8080`.
    - Crie um novo job do tipo `Pipeline`.
    - Em `Pipeline Definition`, selecione a opção `Pipeline script from SCM`.
    - Em `Source Code Management (SCM)`, selecione `Git`.
    - Na seção `Repository URL`, insira a URL do repositório Git:
    `https://github.com/ManelPechim/Trabalho-DevOps-22.8999-9--22.8482-6.git`.
    - Em `Branch Specifier` altere `*/master` para `*/main`.
    - Clique em Salvar e depois clique em `Build Now` para iniciar a execução do pipeline.

4. Acesse o Grafana para visualizar as métricas:
    - Acesse o Grafana em `http://localhost:3000`.
    - Credenciais padrão:
        - Usuário: `admin`
        - Senha: `admin`
    - Após o login, você verá as dashboards configuradas para monitorar as métricas da aplicação, como número de acessos e consultas ao banco de dados.

## Conclusão

Após a execução do pipeline, todos os serviços (Flask, MariaDB, Prometheus, Grafana) devem estar funcionando corretamente. A aplicação estará em execução, o Jenkins terá realizado a automação do processo de build, teste e deploy, e o Grafana estará exibindo as métricas em tempo real coletadas pelo Prometheus.