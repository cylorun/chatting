from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ui.components.Channel import Channel
from user.User import User
from user.Creds import Creds
from ui.components.Form import SignIn, Login

import host
import requests, sys, os, json, threading

class Chatterino:
    def __init__(self, user = None):
        self.user = user
        self.root = Tk()
        self.root.title('Lokaverk')    
        self.root.geometry('600x600')
        self.max_retries = 5
        self.channel_json = f'{os.getcwd()}\\client\\ui\\channels.json'
        self.notebook = ttk.Notebook(self.root)
        self.menu = Menu(self.root)
        
        file_menu = Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Exit", command=self.exit)
        self.menu.add_cascade(label="File",menu=file_menu)
        
        settings_menu = Menu(self.menu, tearoff=0)
        settings_menu.add_command(label='Switch User')
        settings_menu.add_command(label='Add user')
        settings_menu.add_separator()
        settings_menu.add_command(label='Log out', command=self.log_out)
        self.menu.add_cascade(label="Settings", menu=settings_menu)
        
        channel_menu = Menu(self.menu, tearoff=0)
        channel_menu.add_command(label='Add channel')
        channel_menu.add_command(label="Create channel")
        self.menu.add_cascade(label="Channel",menu=channel_menu)
        
        self.root.config(menu=self.menu)
        self.notebook.pack(fill='both', expand=True)

    def log_out(self):
        Creds.remove(User.get_instance().to_dict())
        
    def run(self):
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
            for channel in data:
                if not channel['channel_id'] in loaded:
                    c = Channel(self.notebook, channel['channel_id'])
                    c.wait_for_info()
                    self.notebook.add(c, text=c.info['name'])
    
    def get_loaded_channels(self):
        return [k.channel_id for k in self.notebook.winfo_children() ]
    
    def add_channel(self, channel_name):
        with open(self.channel_json) as file:
            data = json.load(file)
            res = requests.post(f'{host.HOSTNAME}/api/channel_name/', json={'name':channel_name},
                                headers={'Content-Type': 'application/json'}).json()
            channel = Channel(self.notebook,res[0]['channel_id'])
            channel.wait_for_info()
            self.notebook.add(channel,text=channel.info['name'])

    def add_user(self, user):
        req = requests.post(f'{host.HOSTNAME}/api/register', json=user,
                                headers={'Content-Type': 'application/json'}).json()[0] # returns the user with an ID
        req['active'] = True
        self.user = User.get_instance(req)
        Creds.add(req)
        
    def exit(self):
        self.root.destroy()
        sys.exit(1)
            


if __name__ == '__main__':
    def run(user = None):
        app.raise_for_conn()
        if user != None:
            app.add_user(user)
            
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