import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[1]))

from application.core.execution_controller import ExecutionController

from application.GEN.questions.questions import *

app = ExecutionController()

print(app._execution_list)