import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from utils.decorator_catalog_buider import DecoratorCatalogBuider

from infrastructure.messages_service.rabbit_mq_interface import Publisher, Consumer

from domain.ports.mensages_packs_port import BaseMessagePack

import subprocess

_SetupDLB_messagesPacksDict = DecoratorCatalogBuider(id="messagesPackegesList")
_SetupDLB_messagesListeners = DecoratorCatalogBuider(id="messagesListeners")

class MessagesServiceController:

    def __init__(self, durable_exchenge: bool) -> None:
        self._messages_packs = _SetupDLB_messagesPacksDict.get_data()
        self._listeners = _SetupDLB_messagesPacksDict.get_data()

        self.publisher_service = Publisher()

        self.listener_service = Consumer()

        self.__durable_exchenge = durable_exchenge #True -> As mensagens sao salvas em disco pelo exchange do RabbitMQ
    
    @_SetupDLB_messagesPacksDict.create_decorator
    def register_message_packs(self
                               , exchange_name: str
                               , routing_key: str):
        """
        exchange_name: nome da lista de distribuição
        routing_key: nome dos tópicos, com cada assunto separado por '.'
        """
        ...

    def send_to_publisher(self, message_pack: BaseMessagePack):

        """Envia um pacote de mensagem para o servico de mensagens (RabbitMQ)"""

        #Identifica o message_pack e recupera suas propriedades registradas:

        if message_pack.origin_class not in self._messages_packs:
            raise Exception(f"Message pack '{message_pack.__class__.__name__}' was not registered. Use the decorator '' to register it.")
        
        pack_registred_propertys: dict = self._messages_packs[message_pack.origin_class]

        #Configura o publisher e envia:

        self._publisher_service.set_channel(pack_registred_propertys["exchange_name"]
                                           , durable=self.__durable_exchenge)
        
        self._publisher_service.send(routing_key=pack_registred_propertys["exchange_name"]
                                    , exchange=pack_registred_propertys["routing_key"]
                                    , message=message_pack.content
                                    , headers=message_pack.headers
                                    )
    
    @_SetupDLB_messagesListeners.create_decorator
    def register_listener(self
                        , exchange_name: str
                        , binding_keys: str|list = "#"
                        , queue_name=""
                        , exclusive=False
                        , durable=False
                        , auto_delete=True
                        ):
        ...

    def _start_listeners(self):
        """Inicia todos os listeners registrados."""

        self._listeners_process = []

        for k, v in self._listeners.items():
            self._listeners_process(subprocess.Popen(['python', 'x.py', 'teste'], start_new_session=True))

    def get_listener(self, listener_name):
        for k, v in self._listeners.items():
            if k.__class__.__name__ == listener_name:
                return (k, v)
        raise Exception(f"Listener '{listener_name}' not registered. Use @app.message.register_listener(() to do that.")
