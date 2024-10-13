
from abc import ABC, abstractmethod

from domain.value_classes.mensage_status import *

class BaseMessagePack:
    """As implantacoes da classe BaseTaskPackege funcionam para endereçar um objeto 'content' para um local execucao especifico,
    definido no pelo decorator @register_mensage_packege (implementado no mensages_service_controller).
    """

    def __init__(self
                 , origin_class: object = None
                 , input_object_class: object = None
                 , input_object_uuid: str|int = None
                 , content: str|dict = None
                 , headers: dict = dict()
                 ):
        
        self.content = content
        self.headers = headers

        if origin_class:
            self.headers["origin_class"] = origin_class.__name__
        
        if input_object_class:
            self.headers["input_object_class"] = input_object_class.__name__
        
        if input_object_uuid:
            self.headers["input_object_uuid"] = input_object_uuid

    def validate(self):
        ...
        
    def to_dict(self):
        return {
            "catalog": "messages_packs",
            "class_name": self.__class__.__name__,
            "headers": {},
            "body": {"": ""}
        }

    def from_dict(self, dict_content: dict):
        ...