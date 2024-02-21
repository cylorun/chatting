from tkinter import *
import datetime, base64, os
from PIL import Image
from io import BytesIO

class ImageMessage(Frame):
    def __init__(self, parent, message, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(padx=5,pady=5,borderwidth=2, relief="solid")
        self.message_data = message

        self.user_data = self.message_data['owner']
        self.date = ImageMessage.epoch_to_datetime(self.message_data['date'])
        
        self.time_stm_label = Label(self)
        self.message_author_label = Label(self)
        self.message_content_label = Label(self)
        
        self.load()
        
    def load(self):
        self.time_stm_label.configure(text=self.date, font=('Arial', 7, 'italic'))
        self.time_stm_label.pack(side=TOP,anchor=SW)
        
        self.message_author_label.configure(text=self.user_data['name'])
        self.message_author_label.pack(side=TOP,anchor=SW)
        img_data = base64.b64decode(self.message_data['data'])
        if not os.path.exists(f'{os.getcwd()}\\temp\\tmp.png'):
            os.mkdir(f'{os.getcwd()}\\temp')
            image = Image.open(BytesIO(img_data))
            image = image.convert('RGB')
            image.save(f'{os.getcwd()}\\temp\\tmp.png')

        img = PhotoImage(file=f'{os.getcwd()}\\temp\\tmp.png').subsample(3,3)
        self.message_content_label.configure(image=img)
        self.message_content_label.image = img
        self.message_content_label.pack()



    
    @staticmethod
    def epoch_to_datetime(time: int) -> str:
        if time:
            return datetime.datetime.utcfromtimestamp(time)
        return 'Date Missing'