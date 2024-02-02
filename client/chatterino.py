from tkinter import *
from tkinter import messagebox

from ui.components.Channel import Channel
from user.User import User
from user.Creds import Creds
import host
import subprocess, requests, sys

class Chatterino:
    def __init__(self, user):
        self.user = user
        self.win = Tk()
        self.win.title('Lokaverk')    
        self.win.geometry('600x600')
        self.max_retries = 5
        self.good_connection = False
        self.establish_conn()

    def get_owner(self):
        return self.win
    
    def run(self):
        main_room = Channel(app.get_owner())
        main_room.pack()
        self.win.mainloop()
    
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

            


if __name__ == '__main__':
    usr = User.get_instance(Creds.get_active())
    app = Chatterino(usr)
    app.server_on()
    app.establish_conn()
    if app.good_connection:
        app.run()
    else:
        sys.exit(1)