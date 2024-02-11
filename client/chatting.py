from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ui.components.Channel import Channel
from user.User import User
from user.UserManager import UserManager
from ui.components.Form import SignIn, Login
from ui.menu import ToolMenu
from util.logging import Logging
from util.ChannelManager import ChannelManager
import host
import requests, sys, os, json, threading

class Chatterino:
    def __init__(self, user = None):
        self.user = user
        self.root = Tk()
        self.root.title('Lokaverk')    
        self.root.geometry('600x650')
        self.max_retries = 5 
        self.notebook = ttk.Notebook(self.root)
        self.menu = ToolMenu(self)
        
        self.root.config(menu=self.menu)
        self.notebook.pack(fill='both', expand=True)

    def log_out(self):
        UserManager.remove(User.get_instance().to_dict())
        messagebox.showinfo('Restart needed','Please restart the application')        


    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
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
            Logging.error(f'Could not connect to the server, trying {i} more times.')
        Logging.error('Failed to connect to the server, quitting...')
        messagebox.showerror("Server Error","Could not connect to the server")
        sys.exit(1)
    
    def load_channels(self):
        if os.path.exists(ChannelManager.channel_json):
            data = ChannelManager.get_json()
            loaded = self.get_loaded_channels()
            for channel in data['channels']:
                try:
                    if not channel['channel_id'] in loaded:
                        c = Channel(self.notebook, channel['channel_id'], self.remove_channel)
                        c.wait_for_info()
                        self.notebook.add(c, text=c.channel_info['name'])
                except Exception as e:
                    Logging.error(e)
        else:
            ChannelManager.create_json() # is this even needed lol

    def get_loaded_channels(self):
        return [str(k.channel_id) for k in self.notebook.winfo_children() ]
    
    def add_channel(self, channel_name):
        data = ChannelManager.search_from_name(channel_name)
        if not data:
            messagebox.showwarning('Warning', "Channel not found :/")
            return

        channel = Channel(self.notebook, data[0]['channel_id'], self.remove_channel)
        channel.wait_for_info()
        self.notebook.add(channel, text=channel.channel_info['name'])
        self.notebook.select(channel)

        ChannelManager.add_channel(data[0]['channel_id'])


    def create_channel(self, data):
        try:
            name = data['name']
            password = data['password']
        except Exception as e:
            print(e)
            pass
        owner = UserManager.get_active()['user_id']
        res = requests.post(f'{host.HOSTNAME}/api/channel/new', json={"name":name, "password":password,"user_id":owner},
                        headers={'Content-Type': 'application/json'})
        self.add_channel(res.json()['name'])
    
    def remove_channel(self, channel):
        for w in self.notebook.winfo_children():
            if w.channel_id == channel.channel_id:
                w.destroy()
        ChannelManager.remove_channel(channel.channel_id)

        
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
            UserManager.add(user_data)
        elif req.status_code == 402:
            Logging.warn('Login failed, wrong credentials')
            messagebox.showwarning('Login failed','Password or username incorrect')

    def get_active_channel(self):
        try:
            idx = self.notebook.index(self.notebook.select())
            return self.notebook.winfo_children()[idx]
        except Exception:
            return None

    def exit(self):
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
    if UserManager.has_active():
        app.user = User.get_instance(UserManager.get_active())
        run()
    else:
        app.root.withdraw()
        SignIn(callback=run).mainloop()
        app.root.deiconify()
