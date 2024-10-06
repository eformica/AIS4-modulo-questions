from application.app import registry

from domain.ports.mensages_packs_port import BaseMessagePack

#Internal:
@registry.register_message_packs(routing_key="#", exchange_name="Internal")
class Internal_Generic_Message(BaseMessagePack):
    ...

@registry.register_message_packs(routing_key="Command", exchange_name="Internal")
class Internal_Command_Message(BaseMessagePack):
    ...

@registry.register_message_packs(routing_key="Status.Generic", exchange_name="Internal")
class Internal_Status_Generic_Message(BaseMessagePack):
    ...

@registry.register_message_packs(routing_key="Status.Fail", exchange_name="Internal")
class Internal_Status_Fail_Message(BaseMessagePack):
    ...
