import requests

# URL da sua API
url = 'http://127.0.0.1:5000/adicionar_receita'

# Dados que você quer enviar para a API
dados = {'valor': 2000}

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