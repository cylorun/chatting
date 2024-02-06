from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ui.components.Channel import Channel
from user.User import User
from user.Creds import Creds
from ui.components.Form import SignIn, Login
from ui.menu import ToolMenu

import host
import requests, sys, os, json, threading

class Chatterino:
    def __init__(self, user = None):
        self.user = user
        self.root = Tk()
        self.root.title('Lokaverk')    
        self.root.geometry('600x650')
        self.max_retries = 5
        self.channel_json = os.path.join(os.getcwd(),'ui','channels.json') # contains previously opened channels
        self.notebook = ttk.Notebook(self.root)
        self.menu = ToolMenu(self)
        
        self.root.config(menu=self.menu)
        self.notebook.pack(fill='both', expand=True)

    def log_out(self):
        Creds.remove(User.get_instance().to_dict())

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        with open(self.channel_json, 'r') as file:
            last_id = json.load(file)['last']
        last_channel = [c for c in self.notebook.winfo_children() if c.channel_info == last_id]
        if last_channel:
            self.notebook.select(last_channel)
        self.root.mainloop()
    
    def server_on(self):
        try:
            requests.get(f'{host.HOSTNAME}/api/status')
        except Exception:
            return False
        return True

    def raise_for_conn(self):
        for i in range(self.max_retries,0,-1):
            if self.server_on():
                return 
            print(f'Could not connect to the server, trying {i} more times.')
        messagebox.showerror("Server Error","Could not connect to the server")
        sys.exit(1)
    
    def load_channels(self):
        with open(self.channel_json) as file:
            data = json.load(file)
            loaded = self.get_loaded_channels()
            for channel in data['channels']:
                try:
                    if not channel['channel_id'] in loaded:
                        c = Channel(self.notebook, channel['channel_id'], self.remove_channel)
                        c.wait_for_info()
                        self.notebook.add(c, text=c.channel_info['name'])
                except Exception as e:
                    pass
    
    def get_loaded_channels(self):
        return [str(k.channel_id) for k in self.notebook.winfo_children() ]
    
    def add_channel(self, channel_name):
        res = requests.post(f'{host.HOSTNAME}/api/channel_name', json={'name': channel_name},
                            headers={'Content-Type': 'application/json'})
        if res.status_code == 200:
            try:
                res_json = res.json()
                if len(res_json) == 0:
                    messagebox.showwarning('Warning', "Channel not found :/")
                    return

                c = Channel(self.notebook, res_json[0]['channel_id'], self.remove_channel)
                c.wait_for_info()
                self.notebook.add(c, text=c.channel_info['name'])
                self.notebook.select(c)
                if not res_json[0]['channel_id'] in self.all_channel_ids():
                    with open(self.channel_json, 'r') as file:
                        data = json.load(file)
                        data['channels'].append({'channel_id': res_json[0]['channel_id']})

                    with open(self.channel_json, 'w') as file:
                        json.dump(data, file,indent=2)

            except json.decoder.JSONDecodeError:
                messagebox.showwarning('Warning', 'Invalid JSON in the response.')
        else:
            messagebox.showwarning('Warning', f"Failed to add channel. Status code: {res.status_code}")
    
    def all_channel_ids(self):
        with open(self.channel_json) as file:
            return [i for i in json.load(file)['channels']]
        
    def create_channel(self, data):
        try:
            name = data['name']
            password = data['password']
        except Exception as e:
            print(e)
            pass
        owner = Creds.get_active()['user_id']
        res = requests.post(f'{host.HOSTNAME}/api/channel/new', json={"name":name, "password":password,"user_id":owner},
                        headers={'Content-Type': 'application/json'})
        self.add_channel(res.json()['name'])
    
    def remove_channel(self, channel):
        for w in self.notebook.winfo_children():
            if w.channel_info['channel_id'] == channel.channel_info['channel_id']:
                w.destroy()

        with open(self.channel_json, 'r') as file:
            data = json.load(file)

        updated_data = [c for c in data['channels'] if c['channel_id'] != channel.channel_info['channel_id']]
        data['channels'] = updated_data
        with open(self.channel_json, 'w') as file:
            json.dump(data, file, indent=2)

        
    def add_user(self, user, is_login):
        endpoint = '/api/register'
        if is_login:
            endpoint = '/api/login'

        req = requests.post(f'{host.HOSTNAME}{endpoint}', json=user,
                                headers={'Content-Type': 'application/json'}) # returns the user with an ID
        user_data = req.json()
        if req.status_code == 200:
            user_data['active'] = True
            self.user = User.get_instance(user_data)
            Creds.add(user_data)
        elif req.status_code == 402:
            messagebox.showwarning('Login failed','Password or username incorrect')

    def get_active_channel(self):
        try:
            idx = self.notebook.index(self.notebook.select())
            return self.notebook.winfo_children()[idx]
        except Exception:
            return None
    
    def exit(self):
        with open(self.channel_json, 'r') as file:
            data = json.load(file)
            if len(data) >1 and self.get_active_channel() != None:
                data['last'] = self.get_active_channel().channel_info['channel_id']

        with open(self.channel_json, 'w') as file:
            json.dump(data, file, indent=2)

        self.root.destroy()
        sys.exit(1)
            


if __name__ == '__main__':
    def run(is_login = False ,user = None):
        app.raise_for_conn()
        if user != None:
            app.add_user(user, is_login)
            
        threading.Thread(target=app.load_channels, daemon=True).start()
        app.run()

    app = Chatterino()
    app.raise_for_conn()
    if Creds.has_active():
        app.user = User.get_instance(Creds.get_active())
        run()
    else:
        form = SignIn(callback=run)
        form.mainloop()