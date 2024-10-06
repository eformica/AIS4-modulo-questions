import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from config import Settings

from infrastructure.messages_service.rabbit_mq_interface import MessageService

from domain.ports.mensages_packs_port import BaseMessagePack

import subprocess

from utils.singletom import Singleton

class MessagesServiceController:

    def __init__(self, registry, durable_exchenge: bool) -> None:
        self._registry = registry

        self._message_service = MessageService(Settings.RABBITMQ_HOST
                                                , Settings.RABBITMQ_USER
                                                , Settings.RABBITMQ_PASSWORD)

        self.__durable_exchenge = durable_exchenge #True -> As mensagens sao salvas em disco pelo exchange do RabbitMQ


    def send_to_publisher(self, message_pack: BaseMessagePack, propertys: dict):

        """Envia um pacote de mensagem para o servico de mensagens (RabbitMQ)"""

        #Configura o publisher e envia:

        self._message_service.set_channel(propertys["exchange_name"]
                                           , durable=self.__durable_exchenge)
        
        self._message_service.send(routing_key=propertys["routing_key"]
                                    , exchange=propertys["exchange_name"]
                                    , content=message_pack.content
                                    , headers=message_pack.headers
                                    )
        
        print("OK")