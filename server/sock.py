import socket
import threading

def handle_client(client_socket: socket.socket): 
    while True:
        msg = client_socket.recv(1024).decode('utf-8')
        for client in clients:
            client.send()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)

clients = []
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    print(f'Accepted connection from {addr[0]}:{addr[1]}')
    threading.Thread(target=lambda:handle_client(client_socket)).start()
