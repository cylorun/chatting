from tkinter import *
from tkinter import PhotoImage

class ClickableImage(Frame):
    def __init__(self, parent, on_click, src, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.image = PhotoImage(file=src).subsample(20,20)
        self.label = Label(self, image=self.image)
        self.label.bind("<Button-1>", lambda e: on_click(parent))
        self.label.pack()
    