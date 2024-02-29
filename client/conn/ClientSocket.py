import socket, threading


class ClientSocket:
    def __init__(self, server: tuple, callback: callable) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = server
        self.callback = callback
        self.connected = False

    def listen(self):
        threading.Thread(target=self.do_listen, daemon=True).start()

    def connect(self):
        self.socket.connect(self.server_addr)
        self.connected = True

    def send(self, data):
        if self.connected:
            self.socket.send(data.encode('utf-8'))       # not sendall

    def do_listen(self):
        try:
            while True:
                    res = self.get_data()
                    if res:
                        self.callback(res)
        except Exception as e:
            print(f'Error when listening in socket, {e.__str__()}')
            
    def close(self):
        self.socket.close()

    def get_data(self):
        # data = '' # implementation for .sendall()
        # self.socket.settimeout(1)

        # try:
        #     while True:
        #         chunk = self.socket.recv(1024).decode('utf-8')
        #         if not chunk:
        #             break
        #         data += chunk
        # except socket.timeout:
        #     pass

        # return data
        data = self.socket.recv(1024).decode('utf-8')
        return data