import socket, threading

server_address = ('localhost', 5555)

def receive_messages(sock: socket.socket):
    while True:
        res = sock.recv(1024).decode('utf-8')
        if not res:
            break
        print(res)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(server_address)


receive_handler = threading.Thread(target=receive_messages, args=(client,))#threada da moze primat poruke dok pises i saljes svoje
receive_handler.start()

while True:
    msg = input('')
    client.sendall(msg.encode('utf-8'))
    print('sendt',msg)
