from tkinter import *
from tkinter import messagebox

import requests
class SignIn(Toplevel):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame = LabelFrame(self, text="Signin Form")
        self.callback = callback
        Label(self.frame, text="Username").grid(column=1, row=1)
        Label(self.frame, text="Email").grid(column=1, row=2)
        Label(self.frame, text="Password").grid(column=1, row=3)
        Button(self.frame, text="Submit", command=self.submit).grid(column=2,row=5)
        self.psw_var = StringVar()
        self.name_var = StringVar()
        self.email_var = StringVar()
        
        self.name_entry = Entry(self.frame, textvariable=self.name_var)
        self.email_entry = Entry(self.frame, textvariable=self.email_var)
        self.psw_entry = Entry(self.frame, textvariable=self.psw_var)

        self.name_entry.grid(column=3, row=1)
        self.email_entry.grid(column=3, row=2)
        self.psw_entry.grid(column=3, row=3)
        self.frame.pack()
        

    def submit(self):
        if self.name_var.get() and  self.email_var.get() and self.psw_var.get():
            data = {'name':self.name_var.get(),
                    'password':self.psw_var.get(),
                    'email':self.email_var.get()}
            self.callback(data)
            self.destroy()
        else:
            messagebox.showwarning('Unfilled fields','You did not fill out all the fields!!!!')
            
class Login(Toplevel):
    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent, *args, **kwargs)
        self.frame = LabelFrame(self,text="Login Form")


class ChannelForm(Toplevel):
    def __init__(self,callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback
        self.frame = LabelFrame(self,text="Add a channel.")
        self.frame.pack(fill=Y, expand=Y)
        self.channel_var = StringVar()
        self.channel_entry = Entry(self.frame, textvariable=self.channel_var)
        self.channel_entry.pack()
        self.submit_button = Button(self.frame, text="Add", command=self.on_click)
        self.submit_button.pack(side=BOTTOM)
    
    def on_click(self):
        self.callback(self.channel_var.get())
        self.destroy()

