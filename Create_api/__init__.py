from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

app = Flask(__name__)
# Configura o Flask-Talisman para aplicar medidas de segurança automáticas, incluindo forçar HTTPS,
# aplicar uma política de segurança HTTP (CSP) para restringir o carregamento de recursos externos
# e adicionar cabeçalhos de segurança como Strict-Transport-Security (HSTS) e Referrer Policy à aplicação Flask.
talisman = Talisman(app)

#Banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///historico.db"
app.config["SECRET_KEY"] = "b60488cd9d33b316e74ee642a3c3ccfd"

database = SQLAlchemy(app)

from Create_api import routes