import socket
import threading
import json
import util.data
import socket_handler

def handle_client(client_socket: socket.socket):
    while True:
        try:
            data = get_data(client_socket)
            if data:
                command, args = data.split(':', 1)
                handler = commands.get(command, get_messages)
                response = handler(args)
                if response:
                    client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client request: {e}")
            break


def get_data(sock: socket.socket):
    data = ''
    sock.settimeout(1)  # timeout of 1s

    try:
        while True:
            chunk = sock.recv(1024).decode('utf-8')
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass  # Timeout occurred, no more data to receive

    return data

def send_msg(args):
    pass  

def get_messages(args):
    json_data = json.loads(args)
    return str(util.data.select('SELECT * FROM channels WHERE channel_id = 1'))

commands = {
    'GET_MESSAGES': get_messages,
    'SEND_MESSAGE': send_msg
}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))

server.listen(5)
print("Server is listening for incoming connections...")

while True:
    client_socket, addr = server.accept()
    print(f'Accepted connection from {addr[0]}:{addr[1]}')
    threading.Thread(target=handle_client, args=(client_socket,)).start()
