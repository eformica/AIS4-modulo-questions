from domain.value_classes.status import *

from adapters.GEN.questions_base import Questao

from abc import ABC, abstractmethod

class _BaseTaskPackege(ABC):
    """As implantacoes da classe BaseTaskPackege funcionam para endereçar um objeto 'content' para um local execucao especifico,
    definido no metodo send.
    """
    def __init__(self, content: object):
        self.content = content

    def get_values_class(self):
        return self.content.get_values_class()

    @abstractmethod
    def send(self) -> Status:
        ...

class _MixinReceive_Questao(ABC):
    def get_values_class(self):
        return self.content.get_values_class()
    
#Implantacoes:

class LLM_OpenAI_ChatCompletion_Sync(_BaseTaskPackege, _MixinReceive_Questao):
    def __init__(self, content: Questao):
        self.content = content

    def send(self):
        question = self.content.get_question()

class LLM_OpenAI_ChatCompletion_Async(_BaseTaskPackege, _MixinReceive_Questao):
    def __init__(self, content: Questao):
        self.content = content

    def send(self):
        question = self.content.get_question()

#------------------------------------------------------------------------------------
    