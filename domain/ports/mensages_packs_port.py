
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
                 , headers: dict = None
                 ):
        
        self.origin_class = origin_class
        self.input_object_class = input_object_class 
        self.input_object_uuid = input_object_uuid
        self.content = content
        self.headers = headers

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