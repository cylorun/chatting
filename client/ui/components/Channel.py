from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import requests, host, threading, time, os
from ui.components.Message import Message
from ui.components.ImageMessage import ImageMessage
from ui.components.ClickableImage import ClickableImage
from ui.components.UserPresenceLabel import UserPresenceLabel
from util.logging import Logging
from data.user.User import User
from conn.ClientSocket import ClientSocket
from conn.SocketCommands import SocketCommands

class Channel(ttk.Frame):
    def __init__(self, parent, id, on_close, socket: ClientSocket, *args, **kwargs):
        super().__init__(parent.channel_notebook, *args, **kwargs)
        self.id = id
        self.channel_info = {}  # only channel info, no messages or files
        self.on_close = on_close
        self.max_scroll = 0
        self.socket = socket
        self.parent = parent

        
        ClickableImage(self, on_close, os.path.join(os.getcwd(),'assets','images','x_button.png')).pack(side=TOP, anchor=E)
        self.scroll_frame = ttk.Frame(self)
        self.input_frame = ttk.Frame(self)
        self.label = ttk.Label(self)
        self.label.pack(padx=10, pady=5, side=TOP)

        self.message_canvas = Canvas(self.scroll_frame, bg='white', width=580, height=500, scrollregion=(0, 0, 550, 10000))
        self.message_canvas.pack(side='left')

        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient=VERTICAL, command=self.message_canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.message_canvas['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.config(command=self.message_canvas.yview)
        self.message_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.message_frame = ttk.Frame(self.message_canvas)
        self.message_canvas.create_window((0, 10000), window=self.message_frame, anchor='sw')
        self.scroll_frame.pack(side=TOP)

        self.message_var = StringVar()
        self.send_button = ttk.Button(self.input_frame, text="Send",
                                command=lambda: self.send_message(self.message_var.get()))
        self.message_entry = ttk.Entry(self.input_frame, textvariable=self.message_var)

        self.upload_button = ClickableImage(self.input_frame,on_click= lambda e: self.upload_file(), src=os.path.join(os.getcwd(),'assets','images','upload_button.png'))

        self.upload_button.pack(side=RIGHT)
        self.send_button.pack(side=RIGHT)
        self.message_entry.pack(side=LEFT)
        self.input_frame.pack(side=BOTTOM, anchor=SW)

        self.message_canvas.yview_moveto(1.0)
        self.update_channel()
        
    def on_mousewheel(self, event: Event):
        if event.delta < 0:
            self.message_canvas.yview_scroll(1, "units")
        else:
            self.message_canvas.yview_scroll(-1, "units")

    def clear_content(self):
        for w in self.message_frame.winfo_children():
            w.destroy()

    # def message_heights(self):
    #     for w in self.message_frame.winfo_children():
    #         s = w.winfo_geometry().split('x')[1]
    #         print(s)
    #         self.max_scroll += int(s)

    def update_channel(self): 
        res = requests.get(f'{host.API_ADDR}/api/channel/{self.id}')
        if res.status_code == 404:
            print('invalid channel id channel not found')
            return
        
        if res.status_code == 200:
            self.clear_content()
            channel_json =  res.json()
            messages: list = channel_json['messages'] + channel_json['images']
            messages.sort(key=lambda x: x['date'], reverse=True)
            for message in messages:
                if message['type'] == 'msg':
                    Message(self.message_frame, message).pack(side=BOTTOM, anchor=W)
                elif message['type'] == 'img':
                    ImageMessage(self.message_frame, message).pack(side=BOTTOM, anchor=W)
    
    def append_messages(self, new: list):
        current_messages = self.message_frame.winfo_children()
        self.clear_content()
        
        for n in new:
            current_messages.insert(0, n)
        
        for m in current_messages:
            if isinstance(m, Message):
                Message(self.message_frame, m.message_data).pack(side=BOTTOM, anchor=W)
            elif isinstance(m, ImageMessage):
                ImageMessage(self.message_frame, m.message_data).pack(side=BOTTOM, anchor=W)
            elif isinstance(m, UserPresenceLabel):
                UserPresenceLabel(self.message_frame, m.text).pack(side=BOTTOM, anchor=W)

                
    def send_message(self, content: str):
        if content.strip(): # check if it  empty or not
            json = {"user_id":User.get_instance().get_id(),
                    "channel_id":self.id,
                    "content":content}
            
            res = requests.post(f'{host.API_ADDR}/api/send_msg',json=json, headers={'Content-Type': 'application/json'})

            if res.status_code == 404 or res.status_code == 401:
                print(res.text)
                return
            if res.status_code == 200:
                threading.Thread(target=self.update_channel, daemon=True).start()
                self.message_entry.delete(0, END)
                self.socket_message_upd()

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image files', '*.png;*.jpeg;*.gif;*.jpg')])
        if file_path:
            with open(file_path, 'rb') as f:
                user_id = User.get_instance().get_id()
                files = {'file': f}
                res = requests.post(f'{host.API_ADDR}/api/media/upload', files=files, data={'user_id': user_id, "channel_id":self.id})
                if res.status_code == 200:
                    threading.Thread(target=self.update_channel, daemon=True).start()
                    self.socket_message_upd()
                else:
                    print('Failed to upload file')

    def socket_message_upd(self):
        msg = f'{SocketCommands.COMM_MESSAGE_UPDATE}:{{"channel_id":{self.id},"client_id":"{self.parent.CLIENT_ID}"}}'
        self.socket.send(msg)

    def user_leave(self, data):
        user_id = data['user_id']
        res = requests.get(f'{host.API_ADDR}/api/user/{user_id}')
        if res.status_code == 200:
            username = res.json()['name']
            self.append_messages([UserPresenceLabel(self.message_frame, f'{username} left the room.')])
        
    def user_join(self, data):
        user_id = data['user_id']
        res = requests.get(f'{host.API_ADDR}/api/user/{user_id}')
        if res.status_code == 200:
            username = res.json()['name']
            self.append_messages([UserPresenceLabel(self.message_frame, f'{username} joined the room.')])
        