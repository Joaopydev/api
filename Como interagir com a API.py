import requests


#Adicionando Despesa
url = 'http://127.0.0.1:5000/api-finance-professional/adicionar-receita/'

# Dados que você quer enviar para a API
dados ={
    "user": "joao_cf55@hotmail.com",
    "token": "82d05cab1bc600b9d964506637b2d811",
    "tipo" : "Inquilino",
    "valor" : "750",
}
# Fazendo uma solicitação POST para a API com os dados
resposta = requests.post(url, json=dados)
# Imprimindo a resposta da API
print(resposta.json())
