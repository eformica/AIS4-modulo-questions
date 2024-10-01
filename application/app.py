import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[1]))

from application.core.execution_controller import ExecutionController

app = ExecutionController()

from application.Actors.questioners.questioners import *
from adapters.messages_packs.internal_messages_packs import *

#----------------------------------------------------------------------------------------------------

print(app._execution_catalog)
print(app._messages_packs)