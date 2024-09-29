
from abc import ABC, abstractmethod

from domain.value_classes.mensage_status import *

class BaseMessagePack(ABC):
    """As implantacoes da classe BaseTaskPackege funcionam para endereçar um objeto 'content' para um local execucao especifico,
    definido no pelo decorator @register_mensage_packege (implementado no mensages_service_controller).
    """

    def __init__(self
                 , origin_class: object
                 , input_object_class: object 
                 , input_object_uuid: str|int
                 , content: str|dict
                 , heders: dict = None
                 ):
        
        self.origin_class = origin_class
        self.input_object_class = input_object_class 
        self.input_object_uuid = input_object_uuid
        self.content = content
        self.headers = heders

    def to_dict(self):
        ...