from tkinter import *
import datetime
class ImageMessage(Frame):
    def __init__(self, parent, message, is_file = False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(padx=5,pady=5,borderwidth=2, relief="solid")
        self.is_file = is_file
        self.message_data = message

        self.user_data = self.message_data['owner']
        self.date = Message.epoch_to_datetime(self.message_data['date'])
        
        self.time_stm_label = Label(self)
        self.message_author_label = Label(self)
        self.message_content_label = Label(self)
        
        self.load()
        
    def load(self):
        self.time_stm_label.configure(text=self.date, font=('Arial', 7, 'italic'))
        self.time_stm_label.pack(side=TOP,anchor=SW)
        
        self.message_author_label.configure(text=self.user_data['name'])
        self.message_author_label.pack(side=TOP,anchor=SW)
            
        if not self.is_file:
            self.message_data['content'] = Message.format_content(self.message_data['content'])
            self.message_content_label.configure(text=self.message_data['content'])
            self.message_content_label.pack(side=BOTTOM)
        else:
            img = PhotoImage(data=self.message_data['content'])
            self.message_content_label.configure(image=img)
            self.message_content_label.image = img
    
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