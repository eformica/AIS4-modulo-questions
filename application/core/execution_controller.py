import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from config import Settings

from application.core.registry import get_registry

from application.core.messages_service_controller import MessagesServiceController

import dill as pickle

class ExecutionController:

    def __init__(self) -> None:
        self.registry = get_registry()

        self.messages: MessagesServiceController = MessagesServiceController(
            registry = self.registry,
            durable_exchenge=Settings.RABBITMQ_DURABLE_EXCHANGE)
                
    def address(self, obj):
        if type(obj) == dict:
            ...

        elif type(obj) == list:
            ...
            # for k in obj:
            #     self.address(k)

        else:
            catalog, propertys = self.registry.get_object_propertys(obj)

            if catalog == "messages_packs":
                self.messages.send_to_publisher(obj, propertys)

            else:
                ...

#----------------------

# if __name__ == "__main__":
#     ec = ExecutionController()

#     from adapters.messages_packs.internal_messages_packs import Internal_Generic_Message

#     msg = Internal_Generic_Message(content={"teste": "abc"}, headers={"header": "OK"})

#     ec.address(msg)