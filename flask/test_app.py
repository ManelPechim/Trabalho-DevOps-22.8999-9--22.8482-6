import pytest
import json
from faker import Faker

from app import app, db, Aluno  # Importe sua aplicação, o banco e o modelo Aluno
fake = Faker()

@pytest.fixture
def client():
    """
    Configura o cliente de teste para a aplicação Flask.
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mariadb/school_db'  # Altere conforme necessário
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            # Apenas cria as tabelas se não existirem (não remove ao final)
            db.create_all()
        yield client


def test_adicionar_aluno(client):
    """
    Testa o cadastro de um aluno no banco de dados.
    """
    aluno_data = {
        "nome": fake.name(),  # Gera um nome aleatório
        "ra": fake.numerify("##.####-#")  # Gera o RA no formato "00.0000-0"
    }

    print(f"Dados do Aluno: {aluno_data}")  # Imprime os dados do aluno para o terminal

    response = client.post('/alunos', data=json.dumps(aluno_data), content_type='application/json')

    # Imprime a resposta completa para o terminal
    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.data.decode()}")  # Decodifica os dados da resposta em JSON

    assert response.status_code == 201
    assert response.json['message'] == "Aluno adicionado com sucesso!"
