from tkinter import *
import requests, host
from ui.components.Message import Message

class Channel(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.channel_id = 1
        self.info = self.get_channel_info()['channel'][0]
        self.messages = []
        self.scroll_frame = Frame(self)
        self.input_frame = Frame(self)
        self.label = Label(self, text=self.info['name'], bg='red', fg='white', font=('Helvetica', 16))
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
                                  command=lambda: self.send_message({"user_id": 17, "channel_id": self.channel_id,
                                                                     "content": self.message_var.get()}))
        self.message_entry = Entry(self.input_frame, textvariable=self.message_var)

        self.send_button.pack(side=RIGHT)
        self.message_entry.pack(side=LEFT)
        self.input_frame.pack(side=BOTTOM, anchor=SW)

        self.message_canvas.yview_moveto(1.0)
        self.run_tick() 

    def on_mousewheel(self, event):
        if event.delta < 0:
            self.message_canvas.yview_scroll(1, "units")

    def load_content(self, messages: list):
        messages.sort(key=lambda x: x['message_id'], reverse=True)
        self.clear_frame(self.message_frame)
        for message in messages:
            Message(self.message_frame, message=message).pack(side=BOTTOM, anchor=SW)
        print('reloaded all messages!')

    def send_message(self, message):
        if message['content'].strip() != '':
            res = requests.post(f'{host.HOSTNAME}/api/send_msg', json=message,
                                headers={'Content-Type': 'application/json'}).json()
            self.message_entry.delete(0,END)
            self.run_tick(False)
            print(res)

    def get_channel_info(self) -> dict:
        res = requests.get(f'{host.HOSTNAME}/api/channel/{self.channel_id}')
        res.raise_for_status()
        return res.json()

    def clear_frame(self, frame):
        for f in frame.winfo_children():
            f.destroy()

    def run_tick(self, b = True):
        new = self.get_channel_info()['messages']

        if len(new) != len(self.messages):
            self.messages = new
            self.load_content(self.messages)
        if b:
            self.after(5000, self.run_tick)  

