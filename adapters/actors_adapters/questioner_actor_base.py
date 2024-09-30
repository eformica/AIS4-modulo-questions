from abc import ABC, abstractmethod

from adapters.GEN.questions_base import Questao
from adapters.messages.messages_packs import *

from application.app import app

class QuestionerActorBase:

    @abstractmethod
    @property
    def input_object(self) -> object:
        """Deve retornar o objeto de entrada, usado para instanciar a classe.""" 
    
    @abstractmethod
    @property
    def core_object(self) -> Questao:
        """Deve retornar o objeto instanciado com a questao a ser formulada."""
    
    def _on_trigged(self):
        """
        Executado quando um objeto de 'trigger_classes' é satisfeito, somente se todos os objetos de 'dependences' já
        estiverem satisfeitos.
        """

        self.core_object.send_preposition_to_publisher()

    def _on_message_received(self, message: BaseMessagePack):
        """ 
        Executado quando o objeto recebe uma mensagem diretamente.
        O tipo da acao pode ser determinado por um condicional, avaliando o protocolo da mensagem (subclasse de BaseMessagePack).
        """

        if message.__class__ == object:
            ...
    
    def _on_dependence_satisfected(self, dependence_class):
        """ 
        Executado quando um objeto de 'dependences' comunica que foi satisfeito. Atualiza o status da relação de dependencias.
        """

    def _on_status_satisfected():
        """ 
        Executado quando o objeto é satisfeito. Atualiza o status do objeto.
        """

    def _on_status_fail():
        """ 
        Executado quando o objeto falha em algum processo. Atualiza o status do objeto.
        """