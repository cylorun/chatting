from tkinter import *
import datetime, base64, os, secrets, string
from tkinter import ttk

from PIL import Image
from io import BytesIO

class ImageMessage(ttk.Frame):
    def __init__(self, parent, message, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # self.configure(padx=5,pady=5,borderwidth=2, relief="solid")
        self.configure(borderwidth=2, relief="solid")
        self.message_data = message

        self.user_data = self.message_data['owner']
        self.date = ImageMessage.epoch_to_datetime(self.message_data['date'])
        
        self.time_stm_label = ttk.Label(self)
        self.message_author_label = ttk.Label(self)
        self.message_content_label = ttk.Label(self)
        self.image_dir = os.path.join(os.getcwd(),'temp')
        self.file_extension = self.message_data['name'].split('.')[-1]
        self.img_path = os.path.join(os.getcwd(),'temp', f'{self.message_data["image_id"]}.{self.file_extension}')

        self.load()
        
    def load(self):
        try:
            self.time_stm_label.configure(text=self.date, font=('Arial', 7, 'italic'))
            self.time_stm_label.pack(side=TOP,anchor=SW)
            
            self.message_author_label.configure(text=self.user_data['name'], font=('Arial',10,'bold'))
            self.message_author_label.pack(side=TOP,anchor=SW)
            img_data = base64.b64decode(self.message_data['data'])
            if not os.path.exists(self.image_dir):
                os.mkdir(self.image_dir)

            if not any(file.startswith(str(self.message_data["image_id"])) for file in os.listdir(self.image_dir)): # if the image file isnt cached
                image = Image.open(BytesIO(img_data))
                if self.message_data['trans']:
                    image = image.convert('RGBA')
                else:
                    image = image.convert('RGB')
                image.save(self.img_path)

            img = PhotoImage(file=self.img_path).subsample(3,3)
            self.message_content_label.configure(image=img)
            self.message_content_label.image = img
            self.message_content_label.pack()
        except Exception as e:
            self.message_content_label.configure(text=f'Failed to load image\n{e.__str__()}')
            self.message_content_label.pack()





    
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