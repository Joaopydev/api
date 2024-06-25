from app import app, database, bcrypt, api
from flask import request, jsonify, render_template, url_for, flash, redirect, make_response
from app.models import Usuario, Despesa, Receita
from app.forms import FormLogin, FormCriarConta
from flask_login import login_required, login_user, logout_user, current_user
from flask_restful import Resource
@app.route("/", methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=form.lembrar_dados.data)
            flash("Login realizado com sucesso!", "alert-success")
            return redirect(url_for("rota_principal"))
        else:
            flash("Falha no Login. E-mail ou senha inválidos!", "alert-danger")
    return render_template("login.html", form=form)

@app.route("/criar-conta", methods=['GET', 'POST'])
def criar_conta():
    form = FormCriarConta()
    if form.validate_on_submit():
        senha = bcrypt.generate_password_hash(form.senha.data)
        usuario = Usuario(email=form.email.data, senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario)
        flash("Conta criada com sucesso!", "alert-success")
        return redirect(url_for("rota_principal"))
    return render_template("criar_conta.html", form=form)


@app.route("/api-finance-professional", methods=['GET', 'POST'])
@login_required
def rota_principal():
    despesas = Despesa.query.filter_by(id_usuario=current_user.id)
    total_despesa = sum(despesa.valor for despesa in despesas)
    receitas = Receita.query.filter_by(id_usuario=current_user.id)
    total_receita = sum(receita.valor for receita in receitas)
    cofre = total_receita - total_despesa
    return render_template("rota_principal.html", total_receita=total_receita, total_despesa=total_despesa, cofre=cofre, despesas=despesas, receitas=receitas)


@app.route("/instrucoes", methods=["GET"])
@login_required
def comofunciona():
    return render_template("comofunciona.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso!", "alert-success")
    return redirect(url_for("login"))


# Define uma classe para adicionar uma receita
class AdicionarReceita(Resource):
    def post(self):
        dados = request.json
        if not dados:
            return make_response(jsonify({"Erro": "JSON inválido"}))

        usuario = dados.get('user')
        token = dados.get('token')
        if not usuario or not token:
            return make_response(jsonify({"Erro": "Usuário e token precisam ser fornecidos"}))

        user = Usuario.query.filter_by(email=usuario).first()
        if not user or token != user.token:
            return make_response(jsonify({"Erro": "Usuário ou token inválidos"}))

        valor = dados.get('valor')
        tipo = dados.get('tipo')
        if not valor or not tipo:
            return make_response(jsonify({"Erro": "Valor e tipo de despesa precisam ser fornecidos!"}))
        
        try:
            valor = float(valor)
            if valor <= 0:
                raise ValueError("O valor deve ser maior que zero")
        except ValueError as e:
            return {str(e): "O valor dever se um número"}

        receita = Receita(tipo=tipo, valor=valor, id_usuario=user.id)
        database.session.add(receita)
        database.session.commit()
        return make_response(
            jsonify({"Mensagem": "Receita adicionada com sucesso!"})
        )


class AdicionarDespesa(Resource):
    def post(self):
        dados = request.json
        if not dados:
            return make_response(jsonify({"Erro": "JSON inválido"}))

        usuario = dados.get('user')
        token = dados.get('token')
        if not usuario or not token:
            return make_response(jsonify({"Erro": "Usuário e token precisam ser fornecidos"}))

        user = Usuario.query.filter_by(email=usuario).first()
        if not user or token != user.token:
            return make_response(jsonify({"Erro": "Usuário ou token inválidos"}))

        valor = dados.get('valor')
        tipo = dados.get('tipo')
        if not valor or not tipo:
            return make_response(jsonify({"Erro": "Valor e tipo de despesa precisam ser fornecidos!"}))

        despesa = Despesa(tipo=tipo, valor=valor, id_usuario=user.id)
        database.session.add(despesa)
        database.session.commit()
        return make_response(
            jsonify({"mensagem": "Despesa adicionada com sucesso!"}), 201
        )


class RemoverDespesa(Resource):
    def delete(self):
        dados = request.json
        if not dados:
            return make_response(jsonify({"Erro": "Dados não fornecidos!"}))

        usuario = dados.get("user")
        token_usuario = dados.get("token")
        if not usuario or not token_usuario:
            return make_response(jsonify({"Erro": "Usuário e token precisam ser fornecidos!"}))

        user = Usuario.query.filter_by(email=usuario).first()
        if not user or token_usuario != user.token:
            return make_response(jsonify({"Erro": "Usuário ou token inválidos!"}))

        id_despesa = dados.get("id")
        if not id_despesa:
            return make_response(jsonify({"Erro": "Você precisa fornecer o id da despesa que deseja remover!"}))

        try:
            despesa_filtrada = Despesa.query.filter_by(id=id_despesa, id_usuario=user.id).first()
            if not despesa_filtrada:
                return make_response(jsonify({"Erro": "Despesa não encontrada no banco de dados."}))
            database.session.delete(despesa_filtrada)
            database.session.commit()
            return make_response(jsonify({"Mensagem": "Despesa removida com sucesso!"}))
        except Exception as e:
            #Garante que a sessão do banco de dados seja revertida em caso de erro.
            database.session.rollback()
            return make_response(jsonify({"Erro": "A o tentar remover a despesa", "Detalhes": str(e)}))


class RemoverReceita(Resource):
    def delete(self):
        dados = request.json
        if not dados:
            return make_response(jsonify({"Erro": "Dados não fornecidos!"}))

        usuario = dados.get("user")
        token_usuario = dados.get("token")
        if not usuario or not token_usuario:
            return make_response(jsonify({"Erro": "Usuário ou token precisam ser fornecidos!"}))

        user = Usuario.query.filter_by(email=usuario).first()
        if not user or token_usuario != user.token:
            return make_response(jsonify({"Erro": "Usuário e token inválidos!"}))

        id_receita = dados.get("id")
        if not id_receita:
            return make_response(jsonify({"Erro": "Você precisa fornecer o id da receita que deseja remover!"}))

        try:
            receita_filtrada = Receita.query.filter_by(id=id_receita, id_usuario=user.id).first()
            if not receita_filtrada:
                return make_response(jsonify({"Erro": "receita não encontrada no banco de dados."}))
            database.session.delete(receita_filtrada)
            database.session.commit()
            return make_response(jsonify({"Mensagem": "Receita removida com sucesso!"}))
        except Exception as e:
            # Garante que a sessão do banco de dados seja revertida em caso de erro.
            database.session.rollback()
            return make_response(jsonify({"Erro": "A o tentar remover a receita", "Detalhes": str(e)}))


class ObterResumo(Resource):
    def get(self, usuario, token):

        if not usuario or not token:
            return make_response(jsonify({"Erro": "Usuário e token precisam ser fornecidos"}))

        user = Usuario.query.filter_by(email=usuario).first()
        if user and token == user.token:
            # Faz a soma de todas as despesas
            despesas = Despesa.query.filter_by(id_usuario=user.id)
            total_despesa = sum(despesa.valor for despesa in despesas)
            # Faz a soma de todas as receitas
            receitas = Receita.query.filter_by(id_usuario=user.id)
            total_receita = sum(receita.valor for receita in receitas)
            resumo = {
                "total_receita": total_receita,
                "total_despesa": total_despesa,
                "liquido_atual": total_receita - total_despesa,
                "extrato_receitas":[
                    {
                        "id": receita.id,
                        "tipo": receita.tipo,
                        "valor": receita.valor,
                    }for receita in receitas
                ],
                "extrato_despesas":[
                    {
                        "id": despesa.id,
                        "tipo": despesa.tipo,
                        "valor": despesa.valor,
                    }for despesa in despesas
                ],
            }

            # Retorna o resumo em formato JSON com status 200
            return make_response(
                jsonify(resumo), 200
            )
        else:
            return make_response(
                jsonify({"Erro": "Usuário ou token inválidos"})
            )


#Essas linhas associam cada classe de recurso a um endpoint específico da API, para que as solicitações HTTP correspondentes sejam roteadas para os métodos apropriados de cada classe de recurso.
api.add_resource(AdicionarReceita, '/api-finance-professional/adicionar-receita/')
api.add_resource(AdicionarDespesa, '/api-finance-professional/adicionar-despesa/')
api.add_resource(ObterResumo, '/api-finance-professional/obter-resumo/<string:usuario>/<string:token>')
api.add_resource(RemoverDespesa, '/api-finance-professional/remover-despesa/')
api.add_resource(RemoverReceita, '/api-finance-professional/remover-receita')


