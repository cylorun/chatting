import json
import sys
import socket

sys.path.append('/home/alfgrimur/Desktop/school/sem2/forri2/forri2-verk') 
# sys.path.append('C:\\Users\\alfgr7\\Desktop\\school\\forri2\\chatting') 
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
    send_all(msg, clients,[json_data['client_id']]) # FIX NO SINGLE QUEORS

def user_join(args, clients):
    json_data = json.loads(args)
    channel_id = json_data['channel_id']
    user_id = json_data['user_id']
    msg = f'USER_JOIN:{{"channel_id":{channel_id},"user_id":{user_id}}}'
    send_all(msg, clients,[])

def user_leave(args, clients):
        json_data = json.loads(args)
        channel_id = json_data['channel_id']
        user_id = json_data['user_id']
        msg = f'USER_LEAVE:{{"channel_id":{channel_id},"user_id":{user_id}}}'
        send_all(msg, clients,[])
    
def invalid_command(args, clients):
    return f'Invalid command\n{args}'

def send_all(data, clients: list[socket.socket], blacklisted_ids: list):
    for id, client in clients.items():
        if not id in blacklisted_ids: 
            client.sendall(data.encode('utf-8'))


