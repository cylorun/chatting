from tkinter import *
from components.ChatRoom import ChatRoom
class App:
    def __init__(self):
        self.win = Tk()

        self.win.title('Lokaverk')    
        self.win.geometry('600x600')
        
    def get_owner(self):
        return self.win
    
    
    def run(self):
        self.win.mainloop()
        
if __name__ == '__main__':
    app = App()
    main_room = ChatRoom(app.get_owner())
    main_room.pack()
    app.run()