from flask import Flask, request, jsonify
from data import Data
import os, time, datetime


class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.users = []
        self.messages = []
        self.data_base = Data()
        
        @self.app.route('/api/users', methods=['GET'])
        def hello():
            return self.users

        @self.app.route('/api/send_msg', methods=['POST'])
        def send():
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
            
            # curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"John Doe's wife\", \"password\":\"MyWiftUg1yA55F0ck\",\"email\":\"john@doe.com\"}" http://127.0.0.1:25565/api/register        self.load_data()
        self.load_data()
    def load_data(self):
        d = self.data_base.load()
        self.users = d['users']
        self.messages = d['messages']
        
    def run(self, port = 25565):
        self.app.run(debug=True, port=port)

