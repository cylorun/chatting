from tkinter import *
import time, datetime, requests
class Message(Frame):
    def __init__(self, parent, message, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(padx=5,pady=5,borderwidth=2, relief="solid")
        self.message_data = message
        
        self.user_data = self.message_data['owner']
        self.date = self.epoch_to_datetime(self.message_data['date'])
        
        self.time_stm_label = Label(self)
        self.message_author_label = Label(self)
        self.message_content_label = Label(self)
        
        self.load()
        print(f'Loaded message with ID:{self.message_data['message_id']}')
        
    def load(self):
        self.time_stm_label.configure(text=self.date, font=('Arial', 7, 'italic'))
        self.time_stm_label.pack(side=TOP,anchor=SW)
        
        self.message_author_label.configure(text=self.user_data['name'])
        self.message_author_label.pack(side=TOP,anchor=SW)
        
        self.message_content_label.configure(text=self.message_data['content'])
        self.message_content_label.pack(side=BOTTOM)
    
    @staticmethod
    def epoch_to_datetime(time: int) -> str:
        if time != None:
            return datetime.datetime.utcfromtimestamp(time)
        return 'Date Missing'