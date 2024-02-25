import json
import util.data


def get_messages(args):
    json_data = json.loads(args)
    return str(util.data.select('SELECT * FROM channels WHERE channel_id = 1'))
