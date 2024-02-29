from api.routes import App
from util.data import Data
import threading, sys
Data.create_db()
app = App()
app.run()