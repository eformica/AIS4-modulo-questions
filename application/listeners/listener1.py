import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

#from application.app import app

from adapters.listener_base import ListererBase

#@app.messages.register_listener("")
class Listener1(ListererBase):
    def callback(self):


        return None