import socket, threading


class SocketManager:
    def __init__(self, server: tuple, callback: callable) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = server
        self.callback = callback

    def listen(self):
        threading.Thread(target=self._do_listen, daemon=True).start()

    def connect(self):
        self.socket.connect(self.server_addr)

    def send(self, data):
        self.socket.sendall(data)

    def _do_listen(self):
        while True:
            try:
                res = self.get_data()
                self.callback(res)
            except Exception as e:
                print(f'Error when listening in socket, {e.__str__()}')
            
    
    def get_data(self):
        data = ''
        self.socket.settimeout(1)

        try:
            while True:
                chunk = self.socket.recv(1024).decode('utf-8')
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            pass

        return data