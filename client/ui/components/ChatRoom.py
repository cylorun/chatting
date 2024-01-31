from tkinter import *
import requests
class ChatRoom(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.configure(bg='red')
        
        self.label = Label(self, text="Chat Room", bg='red', fg='white', font=('Helvetica', 16))
        self.label.pack(padx=10, pady=10)
    def update_content():
        content = requests.get('localhost:25565/api/channel/1')