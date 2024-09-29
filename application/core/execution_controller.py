import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from application.core.messages_service_controller import MessagesServiceController

from utils.decorator_catalog_buider import DecoratorCatalogBuider

_SetupDLB_ExecutionList = DecoratorCatalogBuider(id="ExecutionController_execution_list")

from typing import Literal

class ExecutionController:

    def __init__(self) -> None:
        self._execution_list = _SetupDLB_ExecutionList.get_data()

        self.messages = MessagesServiceController()
    
    @_SetupDLB_ExecutionList.create_decorator
    def add_to_execution_list(self,
                              trigger_class: list[object] = None,
                              dependences: list[object] = None,
                              mode: Literal["prod", "homolog", "dev"] = "prod",
                              ):
        """Adiciona um modulo de processamento no sistema."""

        #TODO: Validacao dos parametros