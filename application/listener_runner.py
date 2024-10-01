import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[1]))

from application.app import app

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Corre um listener do Serviço de Mensagens (RabbitMQ) cadastrado na aplicacao.')
    parser.add_argument("listener_class_name", help="Nome da classe do tipo ListenerBase registrada.")
    cmd_args = parser.parse_args()

    listener_class = app.messages.get_listener(cmd_args.listener_class_name)

    print(listener_class)



#    app.messages.listener_service.set_consumer()