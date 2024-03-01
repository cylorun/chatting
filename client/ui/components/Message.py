from tkinter import *
from tkinter import ttk
import datetime
class Message(ttk.Frame):
    def __init__(self, parent, message, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # self.configure(padx=5,pady=5,borderwidth=2, relief="solid")
        self.configure(borderwidth=2, relief="solid")

        self.message_data = message

        self.user_data = self.message_data['owner']
        self.date = Message.epoch_to_datetime(self.message_data['date'])
        
        self.time_stm_label = ttk.Label(self)
        self.message_author_label = ttk.Label(self)
        self.message_content_label = ttk.Label(self)
        
        self.load()
        
    def load(self):
        self.time_stm_label.configure(text=self.date, font=('Arial', 7, 'italic'))
        self.time_stm_label.pack(side=TOP,anchor=SW)
        
        self.message_author_label.configure(text=self.user_data['name'], font=('Arial',10,'bold'))
        self.message_author_label.pack(side=TOP,anchor=SW)

        self.message_data['content'] = Message.format_content(self.message_data['content'])
        self.message_content_label.configure(text=self.message_data['content'])
        self.message_content_label.pack(side=BOTTOM)

    
    @staticmethod
    def format_content(content):
        chunked_content = [content[i:i+80] for i in range(0, len(content), 80)]
        formatted_content = '\n'.join(chunked_content)
        return formatted_content
    
    @staticmethod
    def epoch_to_datetime(time: int) -> str:
        if time != None:
            return datetime.datetime.utcfromtimestamp(time)
        return 'Date Missing'