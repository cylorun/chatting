from routes import App
import subprocess, platform, threading, time, os

def run_subp(cmd: list):
    if platform.system() == "Windows":
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen(cmd, start_new_session=True)

threading.Thread(target=lambda:run_subp(['ngrok', 'http', '8080'])).start()

app = App()
app.run()
