from flask import Flask, request, jsonify
from threading import Thread
from rsa import generate_keypair, encrypt, decrypt
import requests

app = Flask(__name__)

# Geração de chaves
public_key, private_key = generate_keypair()
print(f"Minha chave pública: {public_key}")

# Chave pública do peer
peer_public_key = None


@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    cipher = data['cipher']
    msg = decrypt(private_key, cipher)
    print(f"Peer: {msg}")
    return jsonify({'status': 'received'}), 200


@app.route('/public_key', methods=['POST'])
def exchange_key():
    global peer_public_key
    peer_public_key = tuple(request.json['key'])
    print(f"Chave pública do peer: {peer_public_key}")
    return jsonify({'key': list(public_key)}), 200


def send_message():
    while True:
        msg = input("Você: ")
        if peer_public_key:
            cipher = encrypt(peer_public_key, msg)
            try:
                requests.post('http://localhost:5000/receive', json={'cipher': cipher})
            except:
                print("Erro ao enviar mensagem. Verifique se o peer está online.")
        else:
            print("Aguardando troca de chaves...")


def exchange_keys():
    global peer_public_key
    try:
        res = requests.post('http://localhost:5000/public_key', json={'key': list(public_key)})
        peer_public_key = tuple(res.json()['key'])
        print(f"Chave pública do peer recebida: {peer_public_key}")
    except:
        print("Erro na troca de chaves. Verifique se o peer está online.")


if __name__ == '__main__':
    Thread(target=send_message).start()
    exchange_keys()
    app.run(port=5001)
