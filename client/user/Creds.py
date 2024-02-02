import os, json

class Creds:
    cred_file = os.path.join(os.getcwd(), 'client','user', 'users.json')

    @staticmethod
    def list_all():
        with open(Creds.cred_file, 'r') as file:
            return json.load(file)

    @staticmethod
    def get_active():
        users = Creds.list_all()
        for user in users:
            if user['active']:
                return user