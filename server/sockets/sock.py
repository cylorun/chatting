import socket
import threading
import socket_handler as sh

class Sock():

    def __init__(self) -> None:
        self.commands = {
            'GET_MESSAGES': sh.get_messages,
            'SEND_MESSAGE': sh.send_msg
        }

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ('0.0.0.0', 5555)
        self.server.bind(self.addr)

        self.server.listen(5)
        print("Server is listening for incoming connections...")

        while True:
            client_socket, addr = self.server.accept()
            print(f'Accepted connection from {addr[0]}:{addr[1]}')
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket: socket.socket):
        while True:
            try:
                data = self.get_data(client_socket)
                if data:
                    command, args = data.split(':', 1)
                    handler = self.commands.get(command, sh.invalid_command)
                    response = handler(args)
                    if response:
                        client_socket.sendall(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling client request: {e}")
                break


    def get_data(self, sock: socket.socket):
        data = ''
        sock.settimeout(1)  # timeout of 1s

        try:
            while True:
                chunk = sock.recv(1024).decode('utf-8')
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            pass

        return data



Sock()