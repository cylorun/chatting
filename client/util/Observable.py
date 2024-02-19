import threading, time
from tkinter import Variable


class Observable:
    def __init__(self, obs, callback):
        self.b = True
        self.thread = threading.Thread(target=lambda:self.run(obs, callback), daemon=True)
        self.thread.start()

    def run(self, obs: Variable, callback):
        old = obs.get()
        while self.b:
            if old != obs.get():
                old = obs.get()
                callback()
            time.sleep(0.1)

    def stop(self):
        self.b = False