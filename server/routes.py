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

        @self.app.route('/api/media/upload', methods=['POST'])
        def media_upload():
            data = request.get_json()


        @self.app.route('/api/send_msg', methods=['POST'])
        def send_msg():
            data = request.get_json()
            try:
                user_id = data['user_id']
                channel_id = data['channel_id']
                content = data['content']
                file = ['file']
            except Exception as e:
                return jsonify({'Error':e}), 400
            
            message_id = self.data_base.insert("INSERT INTO messages (user_id, channel_id, content, date) VALUES (?,?,?,?)",(user_id, channel_id, content, int(time.time())))
            self.load_data()
            if file != None:
                with open(file,'rb') as f:
                    file_data = f.read()
                file_id = self.data_base.insert("INSERT INTO files (date, file) VALUES (?,?)",(int(time.time()), file_data))
                self.data_base.insert("INSERT INTO messageFile (message_id, file_id) VALUES (?,?)", (message_id, file_id))

                pass
            return jsonify({'Success':200}), 200 
        
        @self.app.route('/api/register',methods=['POST'])
        def register():
            data = request.get_json()
            try:
                name = data['name']
                password = data['password']
                email = data['email']
            except Exception as e:
                return jsonify({'Error, bad request':e}), 400

            if self.data_base.insert('INSERT INTO users (name, email, password, date) VALUES (?,?,?,?)', (name, email, password, int(time.time()))):
                self.load_data()
                return jsonify(self.data_base.select(f"SELECT * FROM users WHERE name='{name}' AND email='{email}' AND password='{password}'")[0]), 200
            else:
                return jsonify({'Failed to insert to DB':"routes.py 46"}), 400
        
        @self.app.route('/api/login', methods=['POST'])
        def login():
            data = request.get_json()
            try:
                name = data['name']
                password = data['password']
            except Exception:
                pass
            
            u = self.data_base.select(f"SELECT * FROM users WHERE name='{name}' AND password='{password}'")
            if len(u) >=1:
                return jsonify(u[0]), 200
            else:
                return jsonify('Login failed'), 402

            
        @self.app.route('/api/channel/<int:channel_id>', methods=['GET'])
        def channel_info(channel_id):
            channel = {"messages":[],"channel":{}}
            for message in self.messages:
                if message['channel_id'] == channel_id:
                    message['owner'] = {'name' : self.user_from_id(message['user_id'])['name']}
                    channel['messages'].append(message)
            channel['channel'] = self.data_base.select(f'SELECT * FROM channels WHERE channel_id = {channel_id}')
            return jsonify(channel)
        

        @self.app.route('/api/channel/new', methods=['POST'])
        def new_channel():
            data = request.get_json()
            try:
                name = data['name']
                password = data['password']
                owner = data['user_id']
            except Exception:
                pass

            if self.data_base.insert('INSERT INTO channels (date, name, password, user_id) VALUES (?,?,?,?)',(int(time.time()), name, password, owner)):
                return jsonify(self.data_base.select(f"SELECT * FROM channels WHERE name='{name}' AND password='{password}' AND user_id='{owner}'")[0]), 200
            return jsonify({'Error':'Failed to insert data into db'}), 400
        

        @self.app.route('/api/channel_name', methods=['POST'])
        def channel_name():
            data = request.get_json()
            try:
                name = data['name']
            except Exception  as e:
                return jsonify({'Error':e}), 400
            return self.data_base.select(f"SELECT * FROM channels WHERE name LIKE '%{name}%'")
        
        @self.app.route('/api/status', methods=['GET'])
        def status():
            return jsonify({'Up':"200"}), 200
        
        # @self.app.route('/api/', methods=['POST'])
        # def
        self.load_data()
        # curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"John Doe's wife\", \"password\":\"MyWiftUg1yA55F0ck\",\"email\":\"john@doe.com\"}" http://127.0.0.1:25565/api/register     





    def user_from_id(self, user_id):
        for user in self.users:
            if user_id == user['user_id']:
                return user
        return {"date":	None,
                "email"	:None,
                "name"	:'DeletedUser',
                "password	":None,
                "user_id"	:"0"}
    
        
    def load_data(self):
        d = self.data_base.load()
        self.users = d['users']
        self.messages = d['messages']
    
    def run(self, port = 25565):
        Logging.info(f'localhost:{port}')
        self.app.run(debug=True, host='0.0.0.0', port=port)

