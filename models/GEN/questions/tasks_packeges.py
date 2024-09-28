from status import *
from questions_base import Questao

from abc import ABC, abstractmethod

from typing import Callable

class _BaseTaskPackege(ABC):
    """As implantacoes da classe BaseTaskPackege funcionam para endereçar um objeto 'content' para um local execucao especifico,
    definido no metodo send.
    """
    def __init__(self, content: object):
        self.content = content

    @abstractmethod
    def send(self) -> Status:
        ...

#Implantacoes:

class LLM_OpenAI_ChatCompletion_Sync(_BaseTaskPackege):
    def __init__(self, content: Questao):
        self.content = content

    def send(self):
        ...

class LLM_OpenAI_ChatCompletion_Async(_BaseTaskPackege):
    def __init__(self, content: Questao):
        self.content = content

    def send(self):
        ...

#------------------------------------------------------------------------------------

class ExecutionController:
    def __init__(self, classe_mae: object
                 , id_objeto_mae: int|None = None):
        
        self.items = {}
        self.classe_mae = classe_mae
        self.id_objeto_mae = id_objeto_mae

        if id_objeto_mae is not None:
            self.recupera_estado_objeto()


    def get_values(self, item_id: str, especific_fields: list = None):

        return self.items[item_id]().content.get_values(especific_fields)

    def add_item(self, item_id: str, item: Callable):

        """Adiciona items ao contexto do controlador. Item deve ser uma função que retorne um objeto do tipo _BaseTaskPackege."""

        self.items[item_id] = (item)

    def send_item(self, item_id):

        """Recupera o objeto _BaseTaskPackege do item e aciona seu método send para enviá-lo para execução."""

        if not self.item_exists(item_id):
            return IndexError(f"Item '{item_id}' not exists.")
        
        return self.items["AnalisePublicoAlvo"]().content.preposicao

    def item_exists(self, search_id):
        if search_id in self.items.keys():
            return True
        else:
            return False

    def recupera_estado_objeto():
        ...

    