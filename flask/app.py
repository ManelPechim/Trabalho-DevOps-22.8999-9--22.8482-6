import time
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from sqlalchemy.exc import OperationalError
from tenacity import retry, wait_fixed, stop_after_attempt, before_log
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuração da chave secreta para sessões
app.config['SECRET_KEY'] = 'chave_secreta_super_secreta'  # Substitua por uma chave segura

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mariadb/school_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o banco de dados e AppBuilder
db = SQLAlchemy(app)
appbuilder = AppBuilder(app, db.session)

# Adicionar Prometheus Metrics
metrics = PrometheusMetrics(app, path='/metrics')
# Remove a necessidade de uma rota personalizada /metrics (cuidado com duplicação).

# Modelo de Aluno - Definição da tabela 'Aluno' no banco de dados
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    disciplinas = db.Column(db.String(200), nullable=False)

# Decorador retry do Tenacity para gerenciar tentativas de conexão ao banco de dados
@retry(
    wait=wait_fixed(5),  # Aguarda 5 segundos entre tentativas
    stop=stop_after_attempt(5),  # Máximo de 5 tentativas
    before=before_log(logger, logging.WARNING)
)
def initialize_database():
    with app.app_context():
        db.create_all()  # Inicializa o banco de dados
        # Criar um usuário administrador padrão
        if not appbuilder.sm.find_user(username='admin'):
            appbuilder.sm.add_user(
                username='admin',
                first_name='Admin',
                last_name='User',
                email='admin@admin.com',
                role=appbuilder.sm.find_role(appbuilder.sm.auth_role_admin),
                password='admin'
            )
        logger.info("Banco de dados inicializado com sucesso.")

# Inicializar o banco de dados com retries
try:
    initialize_database()
except Exception as e:
    logger.error("Não foi possível conectar ao banco de dados após várias tentativas.")
    raise e

# Visão do modelo Aluno para o painel administrativo
class AlunoModelView(ModelView):
    datamodel = SQLAInterface(Aluno)
    list_columns = ['id', 'nome', 'sobrenome', 'turma', 'disciplinas']

# Adicionar a visão do modelo ao AppBuilder
appbuilder.add_view(
    AlunoModelView,
    "Lista de Alunos",
    icon="fa-folder-open-o",
    category="Alunos",
)

# Rota para listar todos os alunos - Método GET
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    output = [{'id': aluno.id, 'nome': aluno.nome, 'sobrenome': aluno.sobrenome, 'turma': aluno.turma, 'disciplinas': aluno.disciplinas} for aluno in alunos]
    return jsonify(output)

# Rota para adicionar um aluno - Método POST
@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    novo_aluno = Aluno(nome=data['nome'], sobrenome=data['sobrenome'], turma=data['turma'], disciplinas=data['disciplinas'])
    db.session.add(novo_aluno)
    db.session.commit()
    logger.info(f"Aluno {data['nome']} {data['sobrenome']} adicionado com sucesso!")
    return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)