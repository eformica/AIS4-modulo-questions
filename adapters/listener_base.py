from abc import ABC, abstractmethod

import dill as pickle

class ListererBase:
    @abstractmethod
    def callback(self):
        """Função a ser executada quando a mensagem é recebida."""

    def decode_body(self, body, headers):
        try:
            if headers["pickle_dumps"] == True:
                body = pickle.loads(body)
        except Exception as err:
            print(err)

            ...

        return body
