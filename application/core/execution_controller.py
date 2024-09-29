import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from utils.decorator_list_buider import DecoratorListBuider

_SetupDLB_ExecutionList = DecoratorListBuider(id="ExecutionController_execution_list")

from typing import Literal

class ExecutionController:

    def __init__(self) -> None:
        self._execution_list = _SetupDLB_ExecutionList.get_list()
    
    @_SetupDLB_ExecutionList.create_decorator
    def add_to_execution_list(self,
                              trigger_class: list[object] = None,
                              dependences: list[object] = None,
                              mode: Literal["prod", "homolog", "dev"] = "prod",
                              ):
        """Adiciona um modulo de processamento no sistema."""

        #TODO: Validacao dos parametros

    def TESTE(self):
        print("QQQQQQQQQQQQQQQQQQQQQQQQQQQ")
        print(self._execution_list)

EC = ExecutionController()

@EC.add_to_execution_list()
class A:
    ...

@EC.add_to_execution_list()
class B:
    ...

print(EC._execution_list)