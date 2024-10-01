import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[1]))

from application.core.execution_controller import ExecutionController

from application.Actors.questioners.questioners import *

from application.listeners.listener1 import *
app = ExecutionController()


#----------------------------------------------------------------------------------------------------

print(app._execution_catalog)
print(app.messages._listeners)