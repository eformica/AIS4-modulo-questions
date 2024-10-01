from abc import ABC, abstractmethod

class ListererBase(ABC):
    @abstractmethod
    def callback(self):
        """Função a ser executada quando a mensagem é recebida."""