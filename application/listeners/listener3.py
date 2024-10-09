import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from application.app import registry

from adapters.listener_base import ListererBase

@registry.register_listener(exchange_name="Internal", binding_keys="#", queue_name="l3_emissor")
class Listener3(ListererBase):
    
    def callback(self, ch, method, properties, body):

        headers = properties.headers
        body = self.decode_body(body, headers)

        print(properties, body)

        return None