import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[1]))

from application.core.execution_controller import ExecutionController

from application.GEN.questions.questions import *

app = ExecutionController()

#Registro dos Listeners:

from application.listeners import listener1
app.messages.register_listener(listener1.listener, routing_key=None, exchange=None)


#----------------------------------------------------------------------------------------------------

print(app._execution_list)