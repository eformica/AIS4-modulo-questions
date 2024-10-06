from utils.decorator_catalog_buider import DecoratorCatalogBuider

import dill as pickle

from typing import Literal

_SetupDLB_ActorsList = DecoratorCatalogBuider(id="actors_list")
_SetupDLB_messagesPacks = DecoratorCatalogBuider(id="messages_packeges")
_SetupDLB_messagesListeners = DecoratorCatalogBuider(id="messages_listeners")

registry_file_path = "components_registry.pickle"

class RegistryController:
    def __init__(self) -> None:
        self._registry = {}

        self._registry["actors"] = _SetupDLB_ActorsList.get_data()
        self._registry["messages_packs"] = _SetupDLB_messagesPacks.get_data()
        self._registry["listeners"] = _SetupDLB_messagesListeners.get_data()

    @_SetupDLB_ActorsList.create_decorator
    def add_to_execution_catalog(self,
                              trigger_classes: list[object] = None,
                              dependences: list[object] = None,
                              mode: Literal["prod", "homolog", "dev"] = "prod",
                              ):
        """Adiciona um modulo de processamento no sistema."""

        #TODO: Validacao dos parametros

    @_SetupDLB_messagesPacks.create_decorator
    def register_message_packs(self
                               , exchange_name: str
                               , routing_key: str):
        """
        exchange_name: nome da lista de distribuição
        routing_key: nome dos tópicos, com cada assunto separado por '.'
        """
        ...

    @_SetupDLB_messagesListeners.create_decorator
    def register_listener(self
                        , exchange_name: str
                        , binding_keys: str|list = "#"
                        , queue_name=""
                        , exclusive=False
                        , durable=False
                        , auto_delete=True
                        ):
        ...

    def save(self):
        f = open(registry_file_path, 'wb')
        pickle.dump(self._registry, f)
        f.close()

def get_registry():
    with open(registry_file_path, 'rb') as f:
        return pickle.load(f)