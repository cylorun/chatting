from tkinter import *
from tkinter import messagebox
from ui.components.ChannelList import ChannelList
from util.Observable import Observable

import requests, threading, host


class SignIn(Toplevel):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame = LabelFrame(self, text="Sign in")
        self.callback = callback
        Label(self.frame, text="Username").grid(column=1, row=1)
        Label(self.frame, text="Email").grid(column=1, row=2)
        Label(self.frame, text="Password").grid(column=1, row=3)
        Button(self.frame, text="Submit", command=self.submit).grid(column=2,row=5)
        Button(self.frame, text="Already have an account?", command=lambda: self.change_type(*args, **kwargs)).grid(column=2,row=6)
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
        self.geometry('450x170+700+400')
        self.resizable(False, False)



    def submit(self):
        if self.name_var.get() and  self.email_var.get() and self.psw_var.get():
            data = {'name':self.name_var.get(),
                    'password':self.psw_var.get(),
                    'email':self.email_var.get()}
            self.destroy()
            self.callback(user=data)
        else:
            messagebox.showwarning('Unfilled fields','You did not fill out all the fields!!!!')
    
    def change_type(self, *args, **kwargs):
        Login(self.callback, *args, **kwargs)
        self.destroy()
            
class Login(Toplevel):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame = LabelFrame(self, text="Login")
        self.callback = callback
        Label(self.frame, text="Username").grid(column=1, row=1)
        Label(self.frame, text="Password").grid(column=1, row=3)
        Button(self.frame, text="Submit", command=self.submit).grid(column=2,row=5)
        Button(self.frame, text="Don't have an account?", command=lambda: self.change_type(*args, **kwargs)).grid(column=2,row=6)

        self.psw_var = StringVar()
        self.name_var = StringVar()
        
        self.name_entry = Entry(self.frame, textvariable=self.name_var)
        self.psw_entry = Entry(self.frame, textvariable=self.psw_var)

        self.name_entry.grid(column=3, row=1)
        self.psw_entry.grid(column=3, row=3)
        self.frame.pack()
        self.geometry('450x150+700+400')
        self.resizable(False, False)

        

    def submit(self):
        if self.name_var.get() and self.psw_var.get():
            data = {'name':self.name_var.get(),
                    'password':self.psw_var.get()}
            self.destroy()
            self.callback(True, data)
        else:
            messagebox.showwarning('Unfilled fields','You did not fill out all the fields!!!!')
    
    def change_type(self, *args, **kwargs):
        SignIn(self.callback, *args, **kwargs)
        self.destroy()


class JoinChannelForm(Toplevel):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callback = callback
        self.geometry('250x150')

        self.label_frame = LabelFrame(self, text="Choose a channel")
        self.label_frame.pack()

        self.loading_label = Label(self.label_frame)
        self.loading_label.pack(side=TOP)

        self.inp_var = StringVar()
        self.inp_field = Entry(self.label_frame, textvariable=self.inp_var)
        self.inp_field.pack(side=TOP)
        self.channel_list = ChannelList(self.label_frame, self.on_choice, None)
        self.channel_list.pack(side=TOP)

        self.obs = Observable(self.inp_var, lambda: self.update_list())
    
    def update_list(self):
        payload = {"name":self.inp_var.get()}
        try:
            self.loading_label.configure(text="Loading...")
            res = requests.post(f'{host.API_ADDR}/api/channel_name', json=payload,
                                    headers={'Content-Type': 'application/json'})
            self.loading_label.configure(text="")
        
            if res.status_code == 200:
                self.channel_list.update(res.json())
            elif res.status_code == 201:
                self.channel_list.update([])
        except Exception: # happens cuz channel_list or loading_label is destroyed
            pass

    def on_choice(self, channel_id):
        self.obs.stop()
        self.callback(channel_id)
        self.destroy()


        



class MakeChannelForm(Toplevel):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback
        self.geometry('350x150')
        self.frame = LabelFrame(self, text="Create a channel.")
        self.frame.pack(fill=BOTH, expand=True)
        self.resizable(False, False)

        self.channel_var = StringVar()
        self.channel_entry = Entry(self.frame, textvariable=self.channel_var)
        self.channel_entry.pack(pady=5)

        self.password_frame = Frame(self.frame)
        self.password_label = Label(self.password_frame, text="Password (optional):")
        self.password_label.pack(side=LEFT)
        self.password_var = StringVar()
        self.password_entry = Entry(self.password_frame, textvariable=self.password_var, show="*")
        self.password_entry.pack(side=LEFT)
        self.show_password_button = Button(self.password_frame, text="Show Password", command=self.toggle_password_entry)
        self.show_password_button.pack(side=LEFT)
        self.password_frame.pack(pady=5)

        self.submit_button = Button(self.frame, text="Create", command=self.on_click)
        self.submit_button.pack(pady=5)

    def toggle_password_entry(self):
        if self.password_entry['show'] == "":
            self.password_entry.config(show="*")
            self.show_password_button.config(text="Show Password")
        else:
            self.password_entry.config(show="")
            self.show_password_button.config(text="Hide Password")

    def on_click(self):
        if self.channel_var.get():
            channel_name = self.channel_var.get()
            password = self.password_var.get() if self.password_var.get() else None
            self.callback({"name":channel_name,
                           "password":password})
            self.destroy()
        else:
            messagebox.showwarning('Missing fields','You did not fill out the required fields.')
