import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from application.app import registry

from adapters.listener_base import ListererBase

from adapters.messages_packs.internal_messages_packs import Internal_Generic_Message

@registry.register_listener(exchange_name="Internal", binding_keys="L3", queue_name="l3_emissor")
class Listener3(ListererBase):
    from application.core.execution_controller import ExecutionController
    
    def callback(self, ch, method, properties, body):
        print(properties, body)

        return None