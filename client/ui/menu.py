from tkinter import *
from user.Creds import Creds
from user.User import User
from ui.components.Form import *


class ToolMenu(Menu):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent.root, *args, **kwargs)


        self.app = parent  # chatting instance

        file_menu = Menu(self, tearoff=0)
        file_menu.add_command(label="Exit", command=self.app.exit)
        self.add_cascade(label="File",menu=file_menu)
        
        settings_menu = Menu(self, tearoff=0)
        settings_menu.add_command(label='Switch User')
        settings_menu.add_command(label='Add user')
        settings_menu.add_separator()
        settings_menu.add_command(label='Log out', command=self.app.log_out)
        self.add_cascade(label="Settings", menu=settings_menu)
        
        channel_menu = Menu(self, tearoff=0)
        channel_menu.add_command(label='Add channel', command=lambda: ChannelForm(self.app.add_channel))
        channel_menu.add_command(label="Create channel")
        self.add_cascade(label="Channel",menu=channel_menu)


        
    