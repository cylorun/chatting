import json
import sys
import socket

sys.path.append('/home/alfgrimur/Desktop/school/sem2/forri2/forri2-verk') 
from server.util.data import Data



def get_messages(args, clients):
    print(args)
    json_data = json.loads(args)
    return str(Data.select(f'SELECT * FROM channels WHERE channel_id = {json_data["channel_id"]}'))

def send_msg(args, clients):
    json_data = json.loads(args)
    pass

def message_update(args, clients):
    json_data = json.loads(args)
    channel_id = json_data['channel_id']
    msg = f'UPDATE:{{"channel_id":{channel_id}}}'
    send_all(msg, clients) # FIX NO SINGLE QUEORS

def invalid_command(args, clients):
    return f'Invalid command\n{args}'

def send_all(data, clients: list[socket.socket]):
    for client in clients:
        client.sendall(data.encode('utf-8'))


