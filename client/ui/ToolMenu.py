from tkinter import *
from data.user.UserManager import UserManager
from data.user.User import User
from ui.components.Form import *
from ui.Theme import Theme


class ToolMenu(Menu):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent.root, *args, **kwargs)

        self.app = parent  # chatting instance

        file_menu = Menu(self, tearoff=0)
        file_menu.add_command(label="Exit", command=self.app.exit)
        self.add_cascade(label="File",menu=file_menu)
        settings_menu = Menu(self, tearoff=0)

        theme_options = Menu(settings_menu, tearoff=0)
        themes = ['light','dark','aurora']
        for theme in themes:
            theme_options.add_command(label=theme,command=lambda theme= theme: Theme.set_theme(theme, self.app.root))

        settings_menu.add_cascade(label='Theme', menu=theme_options)
        settings_menu.add_command(label='My Profile')
        settings_menu.add_separator()
        settings_menu.add_command(label='Log out', command=self.app.log_out)
        self.add_cascade(label="Settings", menu=settings_menu)
        
        channel_menu = Menu(self, tearoff=0)
        channel_menu.add_command(label='Join channel', command=lambda: JoinChannelForm(self.app.root, self.app.add_channel))
        channel_menu.add_command(label="Create channel", command=lambda: MakeChannelForm(self.app.root, self.app.create_channel))
        self.add_cascade(label="Channel",menu=channel_menu)
