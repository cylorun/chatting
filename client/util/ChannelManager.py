import os, json


class ChannelManager:
    channel_json = os.path.join(os.getcwd(),'config','channels.json')
    def __init__(self):
        pass

    @staticmethod
    def add_channel(id):
        with open(ChannelManager.channel_json, 'r') as file:
            data = json.load(file)
            data['channels'].append({'channel_id': id})
            with open(ChannelManager.channel_json, 'w') as file:
                json.dump(data, file, indent=2)

    @staticmethod
    def remove_channel(id):
        with open(ChannelManager.channel_json, 'r') as file:
            data = json.load(file)

        updated_data = [c for c in data['channels'] if c['channel_id'] != id]
        data['channels'] = updated_data
        with open(ChannelManager.channel_json, 'w') as file:
            json.dump(data, file, indent=2)
    @staticmethod
    def get_json() -> list:
        with open(ChannelManager.channel_json) as file:
            return json.load(file)