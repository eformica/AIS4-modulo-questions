from application.app import registry

from domain.ports.mensages_packs_port import BaseMessagePack

#LLMs:
@registry.register_message_packs(routing_key="OpenAI.ChatCompletion.Sync", exchange_name="LLM_Requests")
class Request_LLM_OpenAI_ChatCompletion_Sync(BaseMessagePack):
    ...

@registry.register_message_packs(routing_key="OpenAI.ChatCompletion.Async", exchange_name="LLM_Requests")
class Request_LLM_OpenAI_ChatCompletion_Async(BaseMessagePack):
    ...

@registry.register_message_packs(routing_key="Response.JSON", exchange_name="LLM_Responses")
class Response_LLM_JSON(BaseMessagePack):
    ...

@registry.register_message_packs(routing_key="Response.Text", exchange_name="LLM_Responses")
class Response_LLM_Text(BaseMessagePack):
    ...

@registry.register_message_packs(routing_key="Process.Status", exchange_name="LLM_Responses")
class Response_LLM_Process_Status(BaseMessagePack):
    ...