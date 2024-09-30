from abc import ABC, abstractmethod

from adapters.GEN.questions_base import Questao
from adapters.messages.LLM_messages_packs import *
from adapters.messages.internal_messages_packs import *

from application.app import app

class QuestionerActorBase:

    #Metodos abstratos:

    @abstractmethod
    @property
    def input_object(self) -> object:
        """Deve retornar o objeto de entrada, usado para instanciar a classe.""" 
    
    @abstractmethod
    @property
    def core_object(self) -> Questao:
        """Deve retornar o objeto instanciado com a questao a ser formulada."""


    #Metodos privados:

    def _register_response(self, response: dict):
        ValuesClass = self.core_object.get_values_class()

        Obj = ValuesClass(**response)


    #Implementacoes da classe herdada:
        
    def on_trigged(self):
        """
        Executado quando um objeto de 'trigger_classes' é satisfeito, somente se todos os objetos de 'dependences' já
        estiverem satisfeitos.
        """

        self.core_object.send_preposition_to_publisher()

    def on_message_received(self, message: BaseMessagePack):
        """ 
        Executado quando o objeto recebe uma mensagem diretamente.
        O tipo da acao pode ser determinado por um condicional, avaliando o protocolo da mensagem (subclasse de BaseMessagePack).
        """

        if message.__class__ == Response_LLM_JSON:
            ...
        elif message.__class__ == Response_LLM_Text:
            ...
        elif message.__class__ == Response_LLM_Process_Status:
            ...
        else:
            #Envia um status de erro internamente
            ...

    
    def on_dependence_satisfected(self, dependence_class):
        """ 
        Executado quando um objeto de 'dependences' comunica que foi satisfeito. Atualiza o status da relação de dependencias.
        """

    def on_processing(self):
        """ 
        Executado quando o objeto é satisfeito. Deve atualizar o status do objeto.
        """

    def on_satisfected(self):
        """ 
        Executado quando o objeto é satisfeito. Deve atualizar o status do objeto.
        """

    def on_fail(self):
        """ 
        Executado quando o objeto falha em algum processo. Deve atualizar o status do objeto.
        """