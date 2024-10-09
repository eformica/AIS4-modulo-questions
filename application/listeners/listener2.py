import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from application.app import registry

from adapters.listener_base import ListererBase

@registry.register_listener(exchange_name="Internal", binding_keys="#", queue_name="l2_receptor")
class Listener2(ListererBase):
    def callback(self, ch, method, properties, body):
        print(properties, body)

        return None