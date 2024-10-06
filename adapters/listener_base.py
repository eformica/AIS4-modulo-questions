from abc import ABC, abstractmethod

class ListererBase:
    @abstractmethod
    def callback(self):
        """Função a ser executada quando a mensagem é recebida."""