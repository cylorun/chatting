from tkinter import *
from tkinter import messagebox

from ui.components.Channel import Channel
from user.User import User
from user.Creds import Creds
from ui.components.Form import SignIn, Login

import host
import requests, sys

class Chatterino:
    def __init__(self, user = None):
        self.user = user
        self.win = Tk()
        self.win.title('Lokaverk')    
        self.win.geometry('600x600')
        self.max_retries = 5
        self.good_connection = False

    def run(self):
        self.win.mainloop()
    
    def add_room(self, room):
        room.pack()
        
    def server_on(self):
        try:
            requests.get(f'{host.HOSTNAME}/api/status')
        except Exception:
            return False
        return True

    def establish_conn(self):
        for i in range(self.max_retries,0,-1):
            if self.server_on():
                self.good_connection = True
                return
            print(f'Could not connect to the server, trying {i} more times.')
        messagebox.showerror("Server Error","Could not connect to the server")
        sys.exit(1)

            


if __name__ == '__main__':
    def call(user = None):
        app.establish_conn()
        if user != None:
            
            user = requests.post(f'{host.HOSTNAME}/api/register', json=user,
                                headers={'Content-Type': 'application/json'}).json()[0]
            print(user)
            user['active'] = True
            app.user = user
            Creds.add(user)
        if app.good_connection:
            app.add_room(Channel(app.win, 2))
            app.run()


    app = Chatterino()
    app.establish_conn()
    if Creds.has_active():
        app.user = User.get_instance(Creds.get_active())
        call()
    else:
        form = SignIn(callback=call)
        form.mainloop()