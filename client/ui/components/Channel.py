from tkinter import *
from tkinter import filedialog, messagebox

import requests, host, threading, time, os
from ui.components.Message import Message
from ui.components.ImageMessage import ImageMessage
from ui.components.ClickableImage import ClickableImage
from util.logging import Logging
from data.user.User import User

class Channel(Frame):
    def __init__(self, parent, id, on_close, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.id = id
        self.channel_info = {}  # only channel info, no messages or files
        self.messages = []
        self.tmp_messages = []
        self.on_close = on_close

        
        ClickableImage(self, on_close, os.path.join(os.getcwd(),'assets','images','x_button.png')).pack(side=TOP, anchor=E)
        self.scroll_frame = Frame(self)
        self.input_frame = Frame(self)
        self.label = Label(self)
        self.label.pack(padx=10, pady=5, side=TOP)

        self.message_canvas = Canvas(self.scroll_frame, bg='white', width=580, height=500, scrollregion=(0, 0, 550, 10000))
        self.message_canvas.pack(side='left')

        self.scrollbar = Scrollbar(self.scroll_frame, orient=VERTICAL, command=self.message_canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.message_canvas['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.config(command=self.message_canvas.yview)
        self.message_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.message_frame = Frame(self.message_canvas, bg='white')
        self.message_canvas.create_window((0, 10000), window=self.message_frame, anchor='sw')
        self.scroll_frame.pack(side=TOP)

        self.message_var = StringVar()
        self.send_button = Button(self.input_frame, text="Send", font=('Arial', 8, 'italic'),
                                command=lambda: self.send_message({"user_id": User.get_instance().get_id(), "channel_id": self.id,
                                                                    "content": self.message_var.get()}))
        self.message_entry = Entry(self.input_frame, textvariable=self.message_var)

        self.upload_button = ClickableImage(self.input_frame,on_click= lambda e: self.upload_file(), src=os.path.join(os.getcwd(),'assets','images','upload_button.png'))

        self.upload_button.pack(side=RIGHT)
        self.send_button.pack(side=RIGHT)
        self.message_entry.pack(side=LEFT)
        self.input_frame.pack(side=BOTTOM, anchor=SW)

        self.message_canvas.yview_moveto(1.0)
        # threading.Thread(target=lambda: self.get_channel_info(self.on_info), daemon=True).start()
        self.update_channel()
        
    def on_mousewheel(self, event: Event):
        if event.delta < 0:
            self.message_canvas.yview_scroll(1, "units")
        else:
            self.message_canvas.yview_scroll(-1, "units")

            
    def update_channel(self):
        res = requests.get(f'{host.HOSTNAME}/api/channel/{self.id}')
        if res.status_code == 404:
            print('invalid channel id channel not found')
            return
        if res.status_code == 200:
            channel_json =  res.json()
            messages = channel_json['messages'] + channel_json['images']
            for message in messages:
                if message['type'] == 'msg':
                    Message(self.message_frame, message).pack()
                elif message['type'] == 'img':
                    ImageMessage(self.message_frame, message).pack()

                        
    