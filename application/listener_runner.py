import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[1]))

import logging

from config import Settings

from application.core.registry import get_registry

registry = get_registry()

#Parse dos parametros da linha de comando:

import argparse

parser = argparse.ArgumentParser(description='Corre um listener do Serviço de Mensagens (RabbitMQ) cadastrado na aplicacao.')
parser.add_argument("listener_class_name", help="Nome da classe do tipo ListenerBase registrada.")
cmd_args = parser.parse_args()

#Recupera o objeto do listener:

listener_class, listener_config = registry.get_class_by_name("listeners", cmd_args.listener_class_name)

#Configura o servico de mensageria:

from infrastructure.messages_service.rabbit_mq_interface import MessageService

message_service = MessageService(Settings.RABBITMQ_HOST
                                , Settings.RABBITMQ_USER
                                , Settings.RABBITMQ_PASSWORD)

message_service.set_channel(exchange_name=listener_config["exchange_name"])

message_service.set_consumer(binding_keys=listener_config["binding_keys"]
                                    , queue_name=listener_config["queue_name"]
                                    , exclusive=listener_config["exclusive"]
                                    , auto_delete=listener_config["auto_delete"])

listener_controller = listener_class()

logging.warning(f"===> {listener_class.__name__} EM SERVIÇO!")
logging.warning(f"- configs: {listener_config}")

message_service.start_listener(listener_controller.callback)