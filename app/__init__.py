from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_restful import Api
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
#O Sentry agrega erros duplicados, captura o rastreamento completo da pilha e variáveis locais para depuração e envia e-mails com base em novos erros ou limites de frequência.
sentry_sdk.init(
    dsn="https://c38cae80a23e3f0a48121805adb83104@o4507235153608704.ingest.us.sentry.io/4507235157999616",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
app = Flask(__name__)
# #configurando o Flask para exibir logs detalhados definindo o nível de registro como DEBUG. - Logs de erro
# app.logger.setLevel(logging.DEBUG)
# Configura o Flask-Talisman para aplicar medidas de segurança automáticas, incluindo forçar HTTPS,
# aplicar uma política de segurança HTTP (CSP) para restringir o carregamento de recursos externos
# e adicionar cabeçalhos de segurança como Strict-Transport-Security (HSTS) e Referrer Policy à aplicação Flask.
#content_security_policy: Permitindo que o flask se conecte com as classes css do bootstrap, através do link
talisman = Talisman(
    app,
    content_security_policy={
        'default-src': "'self'",
        'script-src': [
            "'self'",
            'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
            'https://cdn.tailwindcss.com',
            'https://flowbite.com/',
            'https://flowbite.com/docs/images/logo.svg',
            'https://cdn.jsdelivr.net/npm/flowbite@1.5.0/dist/flowbite.js',
        ],
        'style-src': [
            "'self'",
            'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
            'https://cdn.tailwindcss.com',
            "'unsafe-inline'",
            'https://cdn.jsdelivr.net/npm/flowbite@1.5.0/dist/flowbite.js',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css',
        ],
        'img-src': [
            "'self'",
            'data:',  # Permite imagens inline base64
            'https://flowbite.com/docs/images/logo.svg',
            'https://st3.depositphotos.com/1388768/37656/i/600/depositphotos_376566760-stock-photo-api-application-programming-interface-software.jpg',
        ],
        'font-src': [
            "'self'",
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/webfonts/',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/fonts/'
        ],
    }
)

#Permitindo o registro de recursos para API
api = Api(app)

#Banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dadosapi.db"
app.config["SECRET_KEY"] = "b60488cd9d33b316e74ee642a3c3ccfd"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)

#Permitindo migração no banco de dados
migrate = Migrate(app, database)

login_manager = LoginManager(app)
login_manager.login_view = "/"

bcrypt = Bcrypt(app)

from app import routes