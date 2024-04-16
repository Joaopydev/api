from Create_api import app, database
from flask import request, jsonify
from Create_api.models import Transacoes

@app.route("/adicionar-receita", methods=['GET', 'POST'])
def adicionar_receita():
    dados = request.json
    if not dados or not "valor" in dados:
        return jsonify({"erro": "JSON inválido ou valor ausente"}), 400
    try:
        valor = float(dados["valor"])
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
    except ValueError as e:
        return jsonify({e: "O valor deve ser um número."}), 400

    transacao = Transacoes(tipo="receita", valor=valor)
    database.session.add(transacao)
    database.session.commit()
    return jsonify({"mensagem": "Receita adicionada com sucesso!"}), 201

@app.route("/adicionar-despesa", methods=["GET", "POST"])
def adicionar_despesa():
    dados = request.json
    if not dados or not "valor" in dados:
        return jsonify({"erro": "JSON inválido ou valor ausente"}), 400
    try:
        valor = float(dados["valor"])
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
    except ValueError as e:
        return jsonify({e: "O valor deve ser um número."}), 400
    transacao = Transacoes(tipo="despesa", valor=valor)
    database.session.add(transacao)
    database.session.commit()
    return jsonify({"mensagem": "Receita adicionada com sucesso!"}), 200


@app.route("/adicionar-orcamento", methods=["GET", "POST"])
def adicionar_orcamento():
    global orcamento
    dados = request.json
    if not dados or not "valor" in dados:
        return jsonify({"erro": "JSON inválido ou valor ausente"}), 400
    try:
        orcamento = float(dados["valor"])
        if orcamento <= 0:
           raise ValueError("O valor deve ser maior que zero")
    except ValueError as e:
        return jsonify({e: "O valor deve ser um número."}), 400
    return jsonify({"mensagem": "Orçamento definido com sucesso!"}), 200


@app.route("/obter-resumo", methods=["GET", "POST"])
def obter_resumo():
    tabela_historico = Transacoes.query.all()
    total_despesa = sum(transacao.valor for transacao in tabela_historico if transacao.tipo=="despesa")
    total_receita = sum(transacao.valor for transacao in tabela_historico if transacao.tipo=="receita")
    orcamento_restante = orcamento - total_despesa #if orcamento in globals() else None
    resumo = {
        "total_receita": total_receita,
        "total_despesa": total_despesa,
        "orçamento": orcamento,
        "orçamento_restante": orcamento_restante

    }
    return jsonify(resumo), 200

