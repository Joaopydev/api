from Create_api import database

class Transacoes(database.Model):
    id= database.Column(database.Integer, nullable=False, primary_key=True)
    tipo = database.Column(database.String, nullable=False)
    valor = database.Column(database.Float, nullable=False)