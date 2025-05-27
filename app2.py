import socket
import threading
from rsa import generate_keypair, encrypt, decrypt

# Geração de chaves
public_key, private_key = generate_keypair()
print(f"Minha chave pública: {public_key}")

# Socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5000))
print("Conectado ao servidor.")

# Troca de chaves
peer_public_key = eval(client.recv(1024).decode())
print(f"Chave pública do peer: {peer_public_key}")
client.send(str(public_key).encode())

def receive():
    while True:
        data = client.recv(4096)
        if data:
            cipher = eval(data.decode())
            msg = decrypt(private_key, cipher)
            print(f"Peer: {msg}")

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input("Você: ")
    cipher = encrypt(peer_public_key, msg)
    client.send(str(cipher).encode())
