from flask import Flask, request, jsonify
from util.data import Data
from util.logging import Logging
import os, time, datetime, random


class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.users = []
        self.messages = []
        self.data_base = Data()
        
        @self.app.route('/api/users', methods=['GET'])
        def get_users():
            return self.users

        @self.app.route('/api/send_msg', methods=['POST'])
        def send_msg():
            data = request.get_json()
            print(data)
            return jsonify({'sucess':229})    
        
        @self.app.route('/api/register',methods=['POST'])
        def register():
            data = request.get_json()
            try:
                name = data['username']
                password = data['password']
                email = data['email']
            except Exception:
                return jsonify({'Error':400})
            
            if self.data_base.insert('INSERT INTO users (name, email, password, date) VALUES (?,?,?,?)', (name, password, email, int(time.time()))):
                self.load_data()
                return jsonify({"Sucess":data})
            else:
                return jsonify({'Error':400})
            
        @self.app.route('/api/channel/<int:channel_id>', methods=['GET'])
        def channel_info(channel_id):
            channel_messages = []
            for message in self.messages:
                if message['channel_id'] == channel_id:
                    message['owner'] = self.user_from_id(message['user_id'])
                    channel_messages.append(message)
            return jsonify(channel_messages)
            
        # @self.app.route('/api/user', methods=['POST'])
        # def user_from_id():
        #     data = request.get_json()
        #     # {"user_id":"122"}
        #     for user in self.users:
        #         if data['user_id'] == user['user_id']:
        #             return jsonify(user)
                
        #     return jsonify({"date":	None,
        #                     "email"	:"demo@demo.com",
        #                     "name"	:"demo",
        #                     "password	":"demo",
        #                     "user_id"	:"0"})
                
            # curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"John Doe's wife\", \"password\":\"MyWiftUg1yA55F0ck\",\"email\":\"john@doe.com\"}" http://127.0.0.1:25565/api/register       
        self.load_data()
    def user_from_id(self, user_id):
        # {"user_id":"122"}
        for user in self.users:
            if user_id == user['user_id']:
                return user
            
        return {"date":	None,
                        "email"	:"demo@demo.com",
                        "name"	:f'DeletedUser {random.randint(1,12312)}',
                        "password	":"demo",
                        "user_id"	:"0"}
        
    def load_data(self):
        d = self.data_base.load()
        self.users = d['users']
        self.messages = d['messages']
    
    def run(self, port = 25565):
        Logging.info(f'Server up at localhost:{port}')
        self.app.run(debug=True, port=port)

