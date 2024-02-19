from tkinter import *


class ChannelList(Frame):
    def __init__(self, parent, callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callback = callback

    def on_click(self, channel_id):
        self.callback(channel_id)

    def remove_all(self):
        for w in self.winfo_children():
            w.destroy()

    def update(self, channels: list[dict]):
        self.remove_all()
        if channels:
            for ch in channels:
                channel_name = ch['name']
                Button(self, text=channel_name, command=lambda id = ch['channel_id']: self.on_click(id)).pack(side=TOP)
