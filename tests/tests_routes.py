import unittest
from app import app, database
from flask_login import login_user
from app.models import Usuario
class MeusTestes(unittest.TestCase):
    #Método especial que é usado antes de cada teste. Esse método é usado para configurar o ambiente de teste "setUp"
    def setUp(self):
        # Configurar o aplicativo Flask para testes
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        #Cria um cliente de teste para interagir com o aplicativo Flask durante os testes. Isso permite simular solicitações HTTP para suas rotas.
        self.app = app.test_client()
        # Cria um contexto de aplicativo Flask. Isso é necessário para que o aplicativo Flask e suas extensões possam ser acessados dentro do teste.
        self.contexto = app.app_context()
        #Empurra o contexto do aplicativo, ativando-o.
        self.contexto.push()
        # Cria todas as tabelas no banco de dados. Este comando é comumente usado antes dos testes para garantir que o banco de dados esteja configurado corretamente.
        self.test_db = database.create_all()
        with self.app:
            #Simula o login do usuário para dar continuidade no teste, pois a rota necessita estar logado
            usuario_autenticado = Usuario.query.filter_by(email="joao_cf55@hotmail.com").first()
            if usuario_autenticado:
                login_user(usuario_autenticado)

    # Define um método especial que é executado após cada teste. Este método é usado para limpar o ambiente de teste.
    def tearDown(self):
        #Remove a sessão do banco de dados. Isso garante que cada teste tenha seu próprio contexto de banco de dados isolado.
        self.test_db.remove()
        #Remove todas as tabelas do banco de dados. Isso é feito para limpar o banco de dados após o teste.
        self.test_db.drop_all()
        #Remove o contexto do aplicativo. Isso restaura o estado do aplicativo Flask para como estava antes do teste.
        self.contexto.pop()
    #Definindo um método de teste específico para testar a rota principal da aplicação.
    def test_rota_principal(self):
        #Envia uma solicitação GET para a rota /api-finance-professional usando o cliente de teste criado anteriormente.
        resultado = self.app.get('/api-finance-professional')
        #Verifica se o código de status da resposta é igual a 200, o que indica que a rota foi acessada com sucesso. Se o código de status for diferente de 200, o teste falhará.
        print(resultado.data)
        self.assertEqual(resultado.status_code, 200)