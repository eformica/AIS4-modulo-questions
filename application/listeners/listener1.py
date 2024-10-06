import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from application.app import registry

from adapters.listener_base import ListererBase

from application.core.execution_controller import ExecutionController
from adapters.messages_packs.internal_messages_packs import Internal_Generic_Message

@registry.register_listener(exchange_name="Internal", binding_keys="L1", queue_name="l1_emissor")
class Listener1(ListererBase):
    def callback(self, ch, method, properties, body):
        print("Enviando para o L2")
        EC = ExecutionController()
        
        msg = Internal_Generic_Message(content={"TESTE": "do L1"})

        EC.address(msg)

        ...
#        print("XXXXXXXXXXXXXX")
#        print(f" [x] {method.routing_key}:{body}")
#        print(properties.headers)


        return None