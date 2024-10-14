from utils.decorator_catalog_buider import DecoratorCatalogBuider

import dill as pickle

from typing import Literal

class RegistryDict(dict):
    def get_class_by_name(self, catalog, class_name):
        for k, v in self[catalog].items():
            if k.__name__ == class_name:
                return (k, v)
        raise Exception(f"Classe '{class_name}' não encontrada no catálogo '{catalog}'.")
    
    def get_object_propertys(self, obj):
        if not "_registry_catalog" in obj.__class__.__dict__.keys():
            raise Exception(f"'{obj.__name}' não registrado.")
        
        obj_catalog = obj.__class__.__dict__["_registry_catalog"]

        obj_class, obj_propertys = self.get_class_by_name(obj_catalog, obj.__class__.__name__)

        return (obj_catalog, obj_propertys)
    
_SetupDCB_RegistryCatalog = DecoratorCatalogBuider(id="registry_catalog", dict_class=RegistryDict)

registry_file_path = "components_registry.pickle"

class RegistryController:
    def __init__(self) -> None:
        self._registry = _SetupDCB_RegistryCatalog.get_data()

    @_SetupDCB_RegistryCatalog.create_decorator("actors")
    def add_to_execution_catalog(self,
                              trigger_classes: list[object] = None,
                              dependences: list[object] = None,
                              mode: Literal["prod", "homolog", "dev"] = "prod",
                              ):
        """Adiciona um modulo de processamento no sistema."""

        #TODO: Validacao dos parametros

    @_SetupDCB_RegistryCatalog.create_decorator("messages_packs")
    def register_message_packs(self
                               , exchange_name: str
                               , routing_key: str\
                                ):
        """
        exchange_name: nome da lista de distribuição
        routing_key: nome dos tópicos, com cada assunto separado por '.'
        """
        ...

    @_SetupDCB_RegistryCatalog.create_decorator("listeners")
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

def get_registry() -> RegistryDict:
    with open(registry_file_path, 'rb') as f:
        return pickle.load(f)