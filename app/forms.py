from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import Usuario



class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField("Lembrar dados")
    botao_fazer_login = SubmitField("Fazer Login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("Usuário ou senha inválidos")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    confirmacao_email = StringField("Confirmar E-mail", validators=[DataRequired(), Email(), EqualTo("email", message="Os E-mails devem corresponder!")])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("senha", message="As senhas devem corresponder!")])
    botao_criar_conta = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Já existe uma conta com esse E-mail!")

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(email=username.data).first()
        if usuario:
            raise ValidationError("Já existe uma conta com esse Nome de Usuário!")
