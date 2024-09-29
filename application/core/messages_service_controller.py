import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from config import Settings

from utils.decorator_catalog_buider import DecoratorCatalogBuider

from infrastructure.messages_service.rabbit_mq_interface import Publisher

from domain.ports.mensages_packs_port import BaseMessagePack

_SetupDLB_messagesPacksDict = DecoratorCatalogBuider(id="messagesPackegesList")

class MessagesServiceController:

    def __init__(self, durable_exchenge: bool) -> None:
        self._messages_packs = _SetupDLB_messagesPacksDict.get_data()

        self.publisher_service = Publisher()

        self.__durable_exchenge = Settings.RABBITMQ_DURABLE_EXCHANGE #True -> As mensagens sao salvas em disco pelo exchange do RabbitMQ
    
    @_SetupDLB_messagesPacksDict.create_decorator
    def register_mensage_packs(self
                               , exchange_name: str
                               , routing_key: str):
        """exchange_name: nome dos tópicos, com cada assunto separado por '.'"""
        ...

    def publisher(self, message_pack: BaseMessagePack):

        #Identifica o message_pack e recupera suas propriedades registradas:

        if message_pack.origin_class not in self._messages_packs:
            raise Exception(f"Message pack '{message_pack.__class__.__name__}' was not registered. Use the decorator '' to register it.")
        
        pack_registred_propertys: dict = self._messages_packs[message_pack.origin_class]

        #Configura o publisher e envia:

        self.publisher_service.set_channel(pack_registred_propertys["exchange_name"]
                                           , durable=self.__durable_exchenge)
        
        self.publisher_service.send(routing_key=pack_registred_propertys["exchange_name"]
                                    , exchange=pack_registred_propertys["routing_key"]
                                    , message=message_pack.content
                                    , headers=message_pack.headers)