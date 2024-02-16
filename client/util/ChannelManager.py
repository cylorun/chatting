import os, json, host, requests


class ChannelManager:
    channel_json = os.path.join(os.getcwd(),'config','channels.json')
    
    @staticmethod
    def create_json():
        with open(ChannelManager.channel_json, 'w+') as f:
            json.dump({'channels':[]}, f, indent=2)
    
    @staticmethod
    def add_channel(id):
        if not id in ChannelManager.all_ids():
            if os.path.exists(ChannelManager.channel_json):
                with open(ChannelManager.channel_json, 'r') as file:
                    data = json.load(file)
                    data['channels'].append({'channel_id': id})

            else:
                data = {"channels": [{"channel_id": id}]}

            with open(ChannelManager.channel_json, 'w+') as file:
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
    
    @staticmethod
    def search_from_name(name) -> list:
        res = requests.post(f'{host.HOSTNAME}/api/channel_name', json={'name': name},
                    headers={'Content-Type': 'application/json'})
        if res.status_code == 404:
            return None
        return res.json()
    
    @staticmethod
    def all_ids() -> list:
        if os.path.exists(ChannelManager.channel_json):
            with open(ChannelManager.channel_json) as file:
                return [i for i in json.load(file)['channels']]
        return None