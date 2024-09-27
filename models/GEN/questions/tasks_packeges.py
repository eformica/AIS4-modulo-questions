from questions_base import Questao

from abc import ABC, abstractmethod

class Status:
    def __init__(self, mensage, code = None):
        self.mensage = mensage
        self.code = code

class StatusEnviado(Status):
    ...

class StatusProcessado(Status):
    ...

class StatusErro(Exception, Status):
    ...

class __BaseTaskPackege(ABC):
    """As implantacoes da classe BaseTaskPackege funcionam para endereçar um objeto 'content' para um local execucao especifico,
    definido no metodo send.
    """
    def __init__(self, content: object):
        self.content = content

    @abstractmethod
    def send(self) -> Status:
        ...

#Implantacoes:

class LLM_OpenAI_ChatCompletion_Sync(__BaseTaskPackege):
    def __init__(self, content: Questao):
        self.content = content

    def send(self):
        ...

class LLM_OpenAI_ChatCompletion_Async(__BaseTaskPackege):
    def __init__(self, content: Questao):
        self.content = content

    def send(self):
        ...

#------------------------------------------------------------------------------------
class Etapa:
    def __init__(self, *pacotes):
        self.pacotes = pacotes

class Execution_Queue:
    def __init__(self, classe_mae: object
                 , id_objeto_mae: int|None = None):
        
        self.task_list = {}
        self.classe_mae = classe_mae
        self.id_objeto_mae = id_objeto_mae

        if id_objeto_mae is not None:
            self.recupera_estado_objeto()

    def add_item(self, id, item):
        self.task_list[id] = (item)

    def contain(self, search_id):
        if search_id in self.task_list.keys():
            return True
        else:
            return False

    def recupera_estado_objeto():
        ...

    