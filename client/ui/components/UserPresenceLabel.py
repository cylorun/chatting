from tkinter import*

class UserPresenceLabel(Frame):
    def __init__(self, parent, text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.text = text
        self.label = Label(self, text=text, font=('Arial', 9, 'italic'))
        self.label.pack()