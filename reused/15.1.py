import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 65432
def pozdrav(addr):
    print(f"Ahoj uživateli s IP adresou {addr}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)
print("Vítejte v systému ostraVABANK")
print(f"Server naslouchá na {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    print("Někdo se připojil!")
    Thread(target=pozdrav, args=(client_socket, addr)).start()





