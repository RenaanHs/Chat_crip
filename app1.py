import socket
import threading
from rsa import generate_keypair, encrypt, decrypt

# Geração de chaves
public_key, private_key = generate_keypair()
print(f"Minha chave pública: {public_key}")

# Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(1)
print("Aguardando conexão...")

conn, addr = server.accept()
print(f"Conectado a {addr}")

# Troca de chaves
conn.send(str(public_key).encode())
peer_public_key = eval(conn.recv(1024).decode())
print(f"Chave pública do peer: {peer_public_key}")

def receive():
    while True:
        data = conn.recv(4096)
        if data:
            cipher = eval(data.decode())
            msg = decrypt(private_key, cipher)
            print(f"Peer: {msg}")

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input("Você: ")
    cipher = encrypt(peer_public_key, msg)
    conn.send(str(cipher).encode())
