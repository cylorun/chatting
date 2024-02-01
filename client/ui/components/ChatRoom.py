from tkinter import *
import requests, threading
from components.Message import Message

class ChatRoom(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.channel_id = 1
        self.label = Label(self, text="Chat Room", bg='red', fg='white', font=('Helvetica', 16))
        self.label.pack(padx=10, pady=10)

        self.canvas = Canvas(self, bg='white', width=400, height=300, scrollregion=(0, 0, 400, 1000))
        self.canvas.pack(side='left', fill='both', expand=True)

        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas['yscrollcommand'] = self.scrollbar.set


        self.message_frame = Frame(self.canvas, bg='white')
        self.canvas.create_window((0, 0), window=self.message_frame, anchor='nw')

        self.load_content()
        
    def load_content(self):
            res = requests.get(f'http://localhost:25565/api/channel/{self.channel_id}')
            res.raise_for_status()
            messages = res.json()

            for message in messages:
                threading.Thread(target=lambda: Message(self.message_frame, message=message).pack(side=BOTTOM, anchor=SW), daemon=True).start()
