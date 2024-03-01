import socket
import threading, secrets, string
import socket_handler as sh

class Sock():

    def __init__(self):
        self.commands = {
            'GET_MESSAGES': sh.get_messages,
            'SEND_MESSAGE': sh.send_msg,
            'MESSAGE_UPDATE': sh.message_update,
            'USER_JOIN': sh.user_join,
            'USER_LEAVE': sh.user_leave
        }

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ('0.0.0.0', 5555)
        
        self.clients = {}
        
    def run(self):
        self.server.bind(self.addr)
        self.server.listen(5)
        print("listening for incoming connections...")

        while True:
            client_socket, addr = self.server.accept()
            print(f'Accepted connection from {addr[0]}:{addr[1]}')
            id = Sock.generate_rand_str(8)
            self.clients[id] = client_socket
            client_socket.send(f'ASSIGN:{{"id":"{id}"}}'.encode('utf-8'))
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            
    def handle_client(self, client_socket: socket.socket):
        while True:
            try:
                data = self.get_data(client_socket)
                if data:
                    command, args = data.split(':', 1)
                    handler = self.commands.get(command, sh.invalid_command)
                    response = handler(args, self.clients)
                    if response:
                        client_socket.sendall(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling client request: {e}")
                print(f'Ammount of clients: {len(self.clients)}')
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

    def close(self):
        self.server.close()
        
    @staticmethod
    def generate_rand_str(l)->str:
        alphabet = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(alphabet) for i in range(l))
        return random_string
sock = Sock()
try:
    sock.run()
except Exception as e:
    print(e, "\nmain exception")
    sock.close()