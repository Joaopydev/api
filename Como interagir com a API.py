import requests

#Adicionando receita
url = 'http://127.0.0.1:5000/adicionar-receita'

# Dados que você quer enviar para a API
dados = {'valor': 3000}

# Fazendo uma solicitação POST para a API com os dados
resposta = requests.post(url, json=dados)
# Imprimindo a resposta da API
print(resposta.json())

#Adicionando Despesa
url = 'http://127.0.0.1:5000/adicionar-despesa'

# Dados que você quer enviar para a API
dados = {'valor': 1500}

# Fazendo uma solicitação POST para a API com os dados
resposta = requests.post(url, json=dados)
# Imprimindo a resposta da API
print(resposta.json())

#Definindo um orcamento -> Orçamento é uma váriavel global, ele não é salvo no banco de dados.O orçamento sem vai precisar ser definido. Despes e Receita são salvos no banco de dados.
url = 'http://127.0.0.1:5000/adicionar-orcamento'

# Dados que você quer enviar para a API
dados = {'valor': 5000}

# Fazendo uma solicitação POST para a API com os dados
resposta = requests.post(url, json=dados)
# Imprimindo a resposta da API
print(resposta.json())

#Obtendo o resumo das Finanças
url = 'http://127.0.0.1:5000/obter-resumo'

#Fazendo um solicitação GET para a API
resposta = requests.get(url)

#Imprimindo o resumo das Finanças
print(resposta.json())