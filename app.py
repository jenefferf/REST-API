from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth
import random
from random import randint
import requests
import sys

auth = HTTPBasicAuth()
app = Flask(__name__)


listaDeReplicas = []
historico = []
semente = None
coordenador = False
dadosTemp = []

contasBancarias = [
    {
        'conta': 123,
        'saldo': 200
    },
    {
        'conta': 456,
        'saldo': 300
    },
    {
        'conta': 5678,
        'saldo': 300
    }
]


@app.route('/obterContas', methods=['GET'])
def obtemContas():
    return jsonify({'Contas Bancarias': contasBancarias})


@app.route('/acao', methods=['POST'])
def realizaAcao():
    if not request.json or not 'id' in request.json:
        return "Forbiden", 403

    ID = str(request.json.get('id'))


    try:
        operacao = str(request.json.get('operacao'))
    except:
        dadosHist = {
            'id': ID,
            'status': "fail"
        }
        historico.append(dadosHist)
        return "Forbidden", 403
    try:
        conta = int(request.json.get('conta'))
    except:
        dadosHist = {
            'id': ID,
            'status': "fail"
        }
        historico.append(dadosHist)
        return "Forbidden", 403
    try:
        valor = int(request.json.get('valor'))
    except:
        dadosHist = {
            'id': ID,
            'status': "fail"
        }
        historico.append(dadosHist)
        return "Forbidden", 403

    dadosHist = {
        'id': ID,
        'status': "sucess"
        }
    historico.append(dadosHist)

    dados = {
        'id': ID,
        'operacao': operacao,
        'conta': conta,
        'valor': valor
    }
    dadosTemp.append(dados)

    if coordenador:
        rep1 = listaDeReplicas[0]['endpoint']+'/acao'
        rep2 = listaDeReplicas[1]['endpoint']+'/acao'

        r1 = requests.post(rep1, json=dados)
        r2 = requests.post(rep2, json=dados)

        if r1.status_code == 200 and r2.status_code == 200:
            r1 = requests.put(rep1, json={'id': ID})
            r2 = requests.put(rep2, json={'id': ID})
        else:
            r1 = requests.delete(rep1, json={'id': ID})
            r2 = requests.delete(rep2, json={'id': ID})

        if (operacao == "debito"):
            debitarConta(conta, valor)
        elif (operacao == "credito"):
            creditarConta(conta, valor)
        return jsonify({'Operação': dados}), 201

    else:
        return geraDecisao()


@app.route('/acao', methods=['PUT'])
def realizaAcaoPut():
    if not request.json or not 'id' in request.json:
        return "Forbiden", 403

    ID = request.json.get('id')
    dadosHist = {
        'id': ID,
        'status': "sucess"
    }
    historico.append(dadosHist)
    if coordenador:
        return "Bad Request", 400
    else:
        resultado = [
            resultado for resultado in dadosTemp if resultado['id'] == ID]
        operacao = resultado[0]['operacao']
        conta = resultado[0]['conta']
        valor = resultado[0]['valor']

        if operacao == "debito":
            debitarConta(conta, valor)
        elif operacao == "credito":
            creditarConta(conta, valor)
        return "Ok", 200


@app.route('/acao', methods=['DELETE'])
def realizaAcaoDelete():
    if not request.json or not 'id' in request.json:
        return "Forbiden", 403
    ID = request.json.get('id')
    dadosHist = {
        'id': ID,
        'status': "fail"
    }
    historico.append(dadosHist)
    if coordenador:
        return "Bad Request", 400
    else:
        resultado = [
            resultado for resultado in dadosTemp if resultado['id'] == ID]
        dadosTemp.remove(resultado[0])
        return "Ok", 200


@app.route('/historico', methods=['GET'])
def obtemHistorico():
    return jsonify({'Histórico': historico}), 200


@app.route('/replicas', methods=['GET'])
def retornaListaReplicas():
    return jsonify({'Réplicas': listaDeReplicas}), 200


@app.route('/replicas', methods=['POST'])
def adicionaReplicas():
    if not request.json  or not 'replicas' in request.json:
        abort(400)

    replicas = request.json.get('replicas')

    for i in range(len(replicas)):
        ID = replicas[i]['id']
        endpoint = replicas[i]['endpoint']
        r = {
            'id': ID,
            'endpoint': endpoint
        }
        listaDeReplicas.append(r)


    global coordenador
    coordenador = True
    print("Eu sou o coordenador")

    return jsonify({'Réplicas': listaDeReplicas}), 201


@app.route('/replicas', methods=['DELETE'])
def apagaReplicas():
    if len(listaDeReplicas) == 0:
        abort(404)
    listaDeReplicas.clear()
    global coordenador
    coordenador = False
    return jsonify({'Replicas excluídas': True})


@app.route('/semente', methods=['POST'])
def geraSemente():
    if not request.json or not 's' in request.json:
        abort(400)
    try:
        seed = request.json.get('s')
    except:
        abort(400)
    else:
        global semente
        random.seed(semente)
        semente = int(seed)

    return "Created", 201


def geraDecisao():
    num = randint(1, 10)
    if num > 7:
        return jsonify({'Forbidden': 403}), 403
    else:
        return jsonify({'Ok': 200}), 200


def creditarConta(conta, valor):
    resultado = [
        resultado for resultado in contasBancarias if resultado['conta'] == conta]
    saldoAtual = resultado[0]['saldo']
    novoSaldo = saldoAtual + valor
    resultado[0]['saldo'] = novoSaldo


def debitarConta(conta, valor):
    resultado = [
        resultado for resultado in contasBancarias if resultado['conta'] == conta]
    saldoAtual = resultado[0]['saldo']
    novoSaldo = saldoAtual - valor
    resultado[0]['saldo'] = novoSaldo


if __name__ == "__main__":

    app.run(debug=True, host='127.0.0.1', port=int(sys.argv[1]))
