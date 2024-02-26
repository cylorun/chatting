import json
from ..util.data import Data


def get_messages(args):
    json_data = json.loads(args)
    return str(Data.select(f'SELECT * FROM channels WHERE channel_id = {json_data["channel_id"]}'))

def send_msg(args):
    json_data = json.loads(args)
    pass

def invalid_command(args):
    return ('Invalid command\n', args)

