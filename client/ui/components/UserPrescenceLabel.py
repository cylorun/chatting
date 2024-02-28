from tkinter import*

class UserPrescenceLabel(Frame):
    def __init__(self, parent, text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = Label(self, text=text, font=('Arial', 9, 'italic'))