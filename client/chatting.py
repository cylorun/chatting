from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ui.components.Channel import Channel
from data.user.User import User
from data.user.UserManager import UserManager
from ui.components.Form import *
from ui.menu import ToolMenu
from util.logging import Logging
from util.ChannelManager import ChannelManager
from conn.ClientSocket import ClientSocket
from conn.SocketCommands import SocketCommands
import host
import requests, sys, os, json, threading

class Chatterino:
    def __init__(self, user = None):
        self.user = user
        self.root = Tk()
        self.client_socket = ClientSocket(host.SOCKET_ADDR, self.on_socket)
        self.root.title('Lokaverk')    
        self.root.geometry('600x650')
        self.root.resizable(False, False)

        self.max_retries = 5 
        self.channel_notebook = ttk.Notebook(self.root)
        self.menu = ToolMenu(self)
        
        self.root.config(menu=self.menu)
        self.channel_notebook.pack(fill='both', expand=True)
        self.client_socket.connect()
        self.client_socket.listen()

    def log_out(self):
        UserManager.remove(User.get_instance().to_dict())
        messagebox.showinfo('Restart needed','Please restart the application')        


    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.mainloop()
    
    def server_on(self):
        try:
            requests.get(f'{host.API_ADDR}/api/status')
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
                        info = self.get_channel_info(channel['channel_id'])
                        if info:
                            c = Channel(self.channel_notebook, channel['channel_id'], self.remove_channel, self.client_socket,)
                            c.channel_info = info
                            self.channel_notebook.add(c, text=c.channel_info['name'])
                        else:
                            messagebox.showwarning('404',f"Could not load channel {channel['channel_id']}")
                            ChannelManager.remove_channel(channel['channel_id'])
                except Exception as e:
                    Logging.error(e.__str__())
        else:
            ChannelManager.create_json() # is this even needed lol

    def get_loaded_channels(self):
        return [str(k.id) for k in self.channel_notebook.winfo_children() ]
    
    def add_channel(self, channel_id):
        info = self.get_channel_info(channel_id)
        if info:
            channel = Channel(self.channel_notebook, channel_id, self.remove_channel, self.client_socket )
            channel.channel_info = info
            self.channel_notebook.add(channel, text=channel.channel_info['name'])
            self.channel_notebook.select(channel)

            ChannelManager.add_channel(channel_id)
            return
        Logging.error(f'could not add channel with id {channel_id}')

    def get_channel_info(self, channel_id):
        res = requests.get(f'{host.API_ADDR}/api/channel/{channel_id}')
        if res.status_code == 404:
            print(f'Could not load data for channel {channel_id}')
            return None
        if res.status_code == 200:
            return res.json()['channel']

    def create_channel(self, data):  # will sometimes completely freeze when making a new channel
        try:
            name = data['name']
            password = data['password']
        except Exception as e:
            print(e)
        owner = UserManager.get_active()['user_id']
        res = requests.post(f'{host.API_ADDR}/api/channel/new', json={"name":name, "password":password,"user_id":owner},
                        headers={'Content-Type': 'application/json'})
        
        self.add_channel(res.json()['channel_id'])
    
    def remove_channel(self, channel):
        for w in self.channel_notebook.winfo_children():
            if w.id == channel.id:
                w.destroy()
        ChannelManager.remove_channel(channel.id)

        
    def add_user(self, user, is_login):
        endpoint = '/api/register'
        if is_login:
            endpoint = '/api/login'

        req = requests.post(f'{host.API_ADDR}{endpoint}', json=user,
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
            idx = self.channel_notebook.index(self.channel_notebook.select())
            return self.channel_notebook.winfo_children()[idx]
        except Exception:
            return None

    def exit(self):
        self.root.destroy()
        sys.exit(1)
    
    def on_socket(self, data):
        command, args = data.split(':', 1)
        args = json.loads(args)
        print(f'Recived: {command} \n args:{args}\nRaw: {data}')
        if command == SocketCommands.COMM_UPDATE:# this works
            for channel in self.channel_notebook.winfo_children(): 
                if channel.id == int(args['channel_id']):
                    channel.update_channel()



if __name__ == '__main__':
    def run(is_login = False ,user = None):
        app.raise_for_conn()
        if user:
            app.add_user(user, is_login)
            
        threading.Thread(target=app.load_channels, daemon=True).start()
        app.run()

    def pip_install():
        pass

    app = Chatterino()
    app.raise_for_conn()
    if UserManager.has_active():
        app.user = User.get_instance(UserManager.get_active())
        run()
    else:
        SignIn(callback=run).mainloop()