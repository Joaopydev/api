from Create_api import app, database
from flask import request, jsonify
from Create_api.models import Transacoes

# Define a rota para adicionar uma receita
@app.route("/adicionar-receita", methods=['GET', 'POST'])
def adicionar_receita():
    # Obtém os dados da requisição JSON
    dados = request.json
    # Verifica se os dados estão presentes e se o valor está presente nos dados
    if not dados or not "valor" in dados:
        return jsonify({"erro": "JSON inválido ou valor ausente"}), 400
    try:
        # Tenta converter o valor para float e verifica se é maior que zero
        valor = float(dados["valor"])
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
    except ValueError as e:
        # Retorna um erro se o valor não puder ser convertido para float
        return jsonify({e: "O valor deve ser um número."}), 400

    # Cria uma nova transação de receita e a adiciona ao banco de dados
    transacao = Transacoes(tipo="receita", valor=valor)
    database.session.add(transacao)
    database.session.commit()
    return jsonify({"mensagem": "Receita adicionada com sucesso!"}), 201

# Define a rota para adicionar uma despesa
@app.route("/adicionar-despesa", methods=["GET", "POST"])
def adicionar_despesa():
    # Obtém os dados da requisição JSON
    dados = request.json
    # Verifica se os dados estão presentes e se o valor está presente nos dados
    if not dados or not "valor" in dados:
        return jsonify({"erro": "JSON inválido ou valor ausente"}), 400
    try:
        # Tenta converter o valor para float e verifica se é maior que zero
        valor = float(dados["valor"])
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
    except ValueError as e:
        # Retorna um erro se o valor não puder ser convertido para float
        return jsonify({e: "O valor deve ser um número."}), 400
    # Cria uma nova transação de despesa e a adiciona ao banco de dados
    transacao = Transacoes(tipo="despesa", valor=valor)
    database.session.add(transacao)
    database.session.commit()
    return jsonify({"mensagem": "Receita adicionada com sucesso!"}), 200

# Define a rota para adicionar um orçamento
@app.route("/adicionar-orcamento", methods=["GET", "POST"])
def adicionar_orcamento():
    # Define a variável de orçamento como global
    global orcamento
    # Obtém os dados da requisição JSON
    dados = request.json
    # Verifica se os dados estão presentes e se o valor está presente nos dados
    if not dados or not "valor" in dados:
        return jsonify({"erro": "JSON inválido ou valor ausente"}), 400
    try:
        # Tenta converter o valor do orçamento para float e verifica se é maior que zero
        orcamento = float(dados["valor"])
        if orcamento <= 0:
           raise ValueError("O valor deve ser maior que zero")
    except ValueError as e:
        # Retorna um erro se o valor do orçamento não puder ser convertido para float
        return jsonify({e: "O valor deve ser um número."}), 400
    return jsonify({"mensagem": "Orçamento definido com sucesso!"}), 200

# Define a rota para obter um resumo
@app.route("/obter-resumo", methods=["GET", "POST"])
def obter_resumo():
    # Obtém todas as transações do histórico
    tabela_historico = Transacoes.query.all()
    # Calcula o total de despesas e receitas
    total_despesa = sum(transacao.valor for transacao in tabela_historico if transacao.tipo=="despesa")
    total_receita = sum(transacao.valor for transacao in tabela_historico if transacao.tipo=="receita")
    # Calcula o orçamento restante
    orcamento_restante = orcamento - total_despesa #if orcamento in globals() else None
    # Cria um resumo com os totais de receita, despesa, orçamento e orçamento restante
    resumo = {
        "total_receita": total_receita,
        "total_despesa": total_despesa,
        "orçamento": orcamento,
        "orçamento_restante": orcamento_restante
    }
    return jsonify(resumo), 200

