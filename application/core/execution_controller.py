import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from config import Settings
from application.core.messages_service_controller import MessagesServiceController

from utils.decorator_catalog_buider import DecoratorCatalogBuider

from typing import Literal

_SetupDLB_ExecutionList = DecoratorCatalogBuider(id="ExecutionController_execution_list")

class ExecutionController:

    def __init__(self) -> None:
        self._execution_catalog = _SetupDLB_ExecutionList.get_data()

        self.messages = MessagesServiceController(durable_exchenge=Settings.RABBITMQ_DURABLE_EXCHANGE)
    
    @_SetupDLB_ExecutionList.create_decorator
    def add_to_execution_catalog(self,
                              trigger_classes: list[object] = None,
                              dependences: list[object] = None,
                              mode: Literal["prod", "homolog", "dev"] = "prod",
                              ):
        """Adiciona um modulo de processamento no sistema."""

        #TODO: Validacao dos parametros
