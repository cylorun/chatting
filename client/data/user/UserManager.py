import os, json
from data.Dat import Dat

class UserManager:
    cred_file = os.path.join(os.getcwd(),'config', 'users.dat')

    @staticmethod
    def read() -> list:
        if os.path.exists(UserManager.cred_file):
            # with open(UserManager.cred_file, 'r') as file:
            #     return json.load(file)
            return json.loads(Dat.read(UserManager.cred_file))
        return []

    @staticmethod
    def get_active():
        users = UserManager.read()
        if users != []:
            for user in users:
                if user['active']:
                    return user
        

    @staticmethod
    def add(user):
        curr_data = UserManager.read()
        if user not in curr_data:
            data = curr_data
            data.append(user)
            # with open(UserManager.cred_file, 'w+') as file:
            #     json.dump(data, file, indent=2)
            Dat.write(data, UserManager.cred_file)
                
    @staticmethod
    def remove(user):
        data = UserManager.read()
        for u in data:
            if u['user_id'] == user['user_id']:
                data.remove(u)
        # with open(UserManager.cred_file, 'w') as file:
        #     json.dump(data, file, indent=2)
        Dat.write(data, UserManager.cred_file)
            
    @staticmethod
    def set_active(user_id):
        users = UserManager.read()
        for user in users:
            if user['user_id'] == user_id:
                user['active'] = True
            else: 
                user['active'] = False        
        
        # with open(UserManager.cred_file, 'w') as file:
        #         json.dump(users, file, indent=2)
        Dat.write(users, UserManager.cred_file)
                
    @staticmethod
    def has_active():
        return len(UserManager.read()) > 0
    
