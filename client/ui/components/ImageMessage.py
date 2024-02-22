from tkinter import *
import datetime, base64, os, secrets, string
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
        try:
            self.time_stm_label.configure(text=self.date, font=('Arial', 7, 'italic'))
            self.time_stm_label.pack(side=TOP,anchor=SW)
            
            self.message_author_label.configure(text=self.user_data['name'])
            self.message_author_label.pack(side=TOP,anchor=SW)
            img_data = base64.b64decode(self.message_data['data'])
            if not os.path.exists(f'{os.getcwd()}\\temp'):
                os.mkdir(f'{os.getcwd()}\\temp')
            image = Image.open(BytesIO(img_data))
            if self.message_data['trans']:
                image = image.convert('RGBA')
            else:
                image = image.convert('RGB')
            img_path = f'{os.getcwd()}\\temp\\{ImageMessage.generate_rand_str()}.png'
            image.save(img_path)

            img = PhotoImage(file=img_path).subsample(3,3)
            self.message_content_label.configure(image=img)
            self.message_content_label.image = img
            self.message_content_label.pack()
        except Exception as e:
            print(e)




    
    @staticmethod
    def epoch_to_datetime(time: int) -> str:
        if time:
            return datetime.datetime.utcfromtimestamp(time)
        return 'Date Missing'
    
    @staticmethod
    def generate_rand_str()->str:
        alphabet = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(alphabet) for i in range(16))
        return random_string