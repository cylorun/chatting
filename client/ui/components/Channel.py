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
        self.channel_info = {}
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
        self.get_channel_info(self.on_info, False)
        self.run_tick()
        
    def on_mousewheel(self, event):
        if event.delta < 0:
            self.message_canvas.yview_scroll(1, "units")
            
    def on_info(self, res: requests.Response):
        if res.status_code == 404:
            messagebox.showwarning('404 Error',f'Channel with id:{self.id} not found')
            self.on_close(self)
        else:
            data = res.json()
            self.channel_info = data
            self.label.configure(text=self.channel_info['channel']['name'], bg='red', fg='white', font=('Helvetica', 16))
            # self.reload(res,True)

    
    def wait_for_info(self):
        while self.channel_info == {}:
            time.sleep(.1)
            
    def load_content(self, channel_data: list):
        print('loading')
        data = channel_data['messages'] + channel_data['files']
        data.sort(key=lambda x: x['date'], reverse=True)
        self.clear_frame(self.message_frame)
        # self.message_canvas.configure(scrollregion=(0, 0, 550, len(messages)*50))
        for message in data:
            if message['type'] == 'msg':
                Message(self.message_frame, message=message).pack(side=BOTTOM, anchor=SW)
            elif message['type'] == 'img':
                ImageMessage(self.message_frame, message=message).pack(side=BOTTOM, anchor=SW)

                

    def send_message(self, message):
        if message['content'].strip() != '':
            threading.Thread(target=lambda: requests.post(f'{host.HOSTNAME}/api/send_msg', json=message,
                            headers={'Content-Type': 'application/json'}).json(), daemon=True).start()
            self.message_entry.delete(0,END)
    
    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image files', '*.png;*.jpeg;*.gif;*.jpg')])
        if file_path:
            with open(file_path, 'rb') as f:
                user_id = User.get_instance().get_id()
                files = {'file': f}
                res = requests.post(f'{host.HOSTNAME}/api/media/upload', files=files, data={'user_id': user_id, "channel_id":self.id})
                if res.status_code == 200:
                    print('File upload successful')
                else:
                    print('Failed to upload file')
                    print(res.json())

        else:
            print("No file selected.")
            
    def clear_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def get_channel_info(self, callback, thread = True):  # requests from api slow asf basically and really inconsistent speed wise
            def make_request():
                try:
                    res = requests.get(f'{host.HOSTNAME}/api/channel/{self.id}')
                except Exception as e:
                    print(e)

                callback(res)

            if thread:
                threading.Thread(target=make_request).start()
            else:
                make_request()
            
    def run_tick(self):
        self.get_channel_info(self.reload)
        self.after(5000, self.run_tick)
        
    def reload(self, res, force = False):
        if res.status_code == 404:
            Logging.error('404 Not found, when updating messages')
        elif res.status_code == 200:
            data = res.json()
            if len(data) != len(self.channel_info) or force: # basically a race condition with self.on_inf0(), then messages get weirdly ordered due tO THIs aswell
                self.channel_info = data
                threading.Thread(target=lambda:self.load_content(data), daemon=True).start() 
            


# just rewrite the entire class at this point lol