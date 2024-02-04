from tkinter import *
import requests, host, threading, time, os
from ui.components.Message import Message
from ui.components.ClickableImage import ClickableImage
from user.User import User

class Channel(Frame):
    def __init__(self, parent, id, on_close, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.channel_id = id
        self.channel_info = {}
        self.messages = []
        self.tmp_messages = []
        tmp_user = User.get_instance()
        self.user ={'name' : tmp_user.get_name(),
                    'user_id' : tmp_user.get_id(),
                    'password' : tmp_user.get_password(),
                    'email' : tmp_user.get_email()}
        
        ClickableImage(self, on_close, f"{os.getcwd()}\\client\\ui\\x_button.png").pack(side=TOP, anchor=E)
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
                                command=lambda: self.send_message({"user_id": self.user['user_id'], "channel_id": self.channel_id,
                                                                    "content": self.message_var.get()}))
        self.message_entry = Entry(self.input_frame, textvariable=self.message_var)

        self.send_button.pack(side=RIGHT)
        self.message_entry.pack(side=LEFT)
        self.input_frame.pack(side=BOTTOM, anchor=SW)

        self.message_canvas.yview_moveto(1.0)
        threading.Thread(target=lambda: self.get_channel_info(self.on_info), daemon=True).start()
        self.run_tick()
        
    def on_mousewheel(self, event):
        if event.delta < 0:
            self.message_canvas.yview_scroll(1, "units")
            
    def on_info(self, info):
        self.channel_info = info['channel'][0]
        self.label.configure(text=self.channel_info['name'], bg='red', fg='white', font=('Helvetica', 16))
    
    def wait_for_info(self):
        while self.channel_info == {}:
            time.sleep(.1)
            
    def load_content(self, messages: list):
        messages.sort(key=lambda x: x['message_id'], reverse=True)
        self.clear_frame(self.message_frame)
        for message in messages:
            Message(self.message_frame, message=message).pack(side=BOTTOM, anchor=SW)

    def send_message(self, message):
        if message['content'].strip() != '':
            threading.Thread(target=lambda:requests.post(f'{host.HOSTNAME}/api/send_msg', json=message,
                                headers={'Content-Type': 'application/json'}).json(), daemon=True).start()
            self.message_entry.delete(0,END)
            # self.get_channel_info(self.reload)


    def clear_frame(self, frame):
        for f in frame.winfo_children():
            f.destroy()

    def get_channel_info(self, callback):  # requests from api slow asf basically and really inconsistent speed wise
            def make_request():
                try:
                    res = requests.get(f'{host.HOSTNAME}/api/channel/{self.channel_id}')
                    res.raise_for_status()
                    result = res.json()
                except Exception as e:
                    raise Exception

                callback(result)

            thread = threading.Thread(target=make_request)
            thread.start()
            
    def run_tick(self):
        self.get_channel_info(self.reload)
        self.after(5000, self.run_tick)
        
    def reload(self, updated_messages):
        updated_messages = updated_messages['messages']
        if len(updated_messages) != len(self.messages):
            self.messages = updated_messages
            threading.Thread(target=lambda:self.load_content(self.messages), daemon=True).start()
            


