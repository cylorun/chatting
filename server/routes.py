from flask import Flask, request, jsonify
from util.data import Data
from util.logging import Logging
from werkzeug.utils import secure_filename

import os, time, datetime, random, hashlib


class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.messages = []
        self.data_base = Data()
        
        @self.app.route('/api/users', methods=['GET'])
        def get_users():
            users = self.data_base.select('SELECT * FROM users')
            if users:
                return users
            return []


        @self.app.route('/api/media/upload', methods=['POST'])
        def media_upload():
            data = request.form
            try:
                file = request.files['file']
                file_name = secure_filename(file.filename)
                user_id = data['user_id']
                channel_id = data['channel_id']
            except Exception:
                return jsonify('Bad request'), 401

            file_id = self.data_base.insert("INSERT INTO files (date, file, user_id, channel_id, name) VALUES (?,?,?,?)",(int(time.time()), file.read(), user_id, channel_id ,file_name))
            return jsonify({'Success':f'File upload successful, file_id  {file_id}'}),200

        @self.app.route('/api/send_msg', methods=['POST'])
        def send_msg():
            data = request.get_json()
            try:
                user_id = data['user_id']
                channel_id = data['channel_id']
                content = data['content']
            except Exception as e:
                return jsonify({'Error':e}), 400
            
            message_id = self.data_base.insert("INSERT INTO messages (user_id, channel_id, content, date) VALUES (?,?,?,?)",(user_id, channel_id, content, int(time.time())))
            
            return jsonify("Uploaded message successfully!"), 200 
        
        @self.app.route('/api/register', methods=['POST'])
        def register():
            data = request.get_json()
            try:
                name = data['name']
                password = data['password']
                email = data['email']
            except Exception as e:
                return jsonify({'Error, bad request':e}), 400
            password = hashlib.sha256(password.encode()).hexdigest()
            if self.data_base.insert('INSERT INTO users (name, email, password, date) VALUES (?,?,?,?)', (name, email, password, int(time.time()))):
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
            password = hashlib.sha256(password.encode()).hexdigest()
            u = self.data_base.select(f"SELECT * FROM users WHERE name='{name}' AND password='{password}'")
            if len(u) >=1:
                return jsonify(u[0]), 200
            else:
                return jsonify('Login failed'), 402

        
        @self.app.route('/api/channel/<int:channel_id>', methods=['GET'])
        def channel_info(channel_id):
            channel = {"messages": [], "files":[], "channel": {}}
            messages = self.data_base.select(f'SELECT * FROM messages')
            channel_data = self.data_base.select(f'SELECT * FROM channels WHERE channel_id = {channel_id}')
            channel_files = self.data_base.select(f'SELECT * FROM files WHERE channel_id == {channel_id}')


            if not channel_data:
                return jsonify({"error": "Channel not found"}), 404
            
            if channel_files:
                channel['files'] = channel_files

            if messages:
                for message in messages:
                    if message['channel_id'] == channel_id:
                        message['owner'] = {'name': self.user_from_id(message['user_id'])['name']}
                        channel['messages'].append(message)

            channel['channel'] = channel_data
            return jsonify(channel), 200


        @self.app.route('/api/channel/new', methods=['POST'])
        def new_channel():
            data = request.get_json()
            try:
                name = data['name']
                password = data['password']
                owner = data['user_id']
            except Exception:
                return jsonify({'Error':'bad req'}), 401

            if self.data_base.insert('INSERT INTO channels (date, name, password, user_id) VALUES (?,?,?,?)',(int(time.time()), name, password, owner)):
                return jsonify(self.data_base.select(f"SELECT * FROM channels WHERE name='{name}' AND password='{password}' AND user_id='{owner}'")[0]), 200
            
            return jsonify({'Error':'Failed to insert data'}), 400
        

        @self.app.route('/api/channel_name', methods=['POST']) # returns a list of all channels(data) which names contain the "name" key
        def channel_name():
            data = request.get_json()

            try:
                name = data['name']
            except Exception  as e:
                return jsonify({'missing params':e}), 401 # bad request
            
            channels = self.data_base.select(f"SELECT * FROM channels WHERE name LIKE '%{name}%'")

            if not channels:
                return jsonify("Error, channel not found"), 201
            
            return jsonify(channels), 200
        
        @self.app.route('/api/status', methods=['GET'])
        def status():
            return jsonify({'Success':"ALl good!!!!!!!!!!"}), 200
        

    def user_from_id(self, user_id) -> dict:
        user = self.data_base.select(f"SELECT * FROM users WHERE user_id == {user_id}")
        if user:
            return user[0]
        
        return {"date":	None,
                "email"	:None,
                "name"	:'DeletedUser',
                "password	":None,
                "user_id"	:"0"}
    
    def run(self, port = 25565):
        Logging.info(f'localhost:{port}')
        self.app.run(debug=True, host='0.0.0.0', port=port)

