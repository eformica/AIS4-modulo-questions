from application.app import app

from domain.ports.mensages_packs_port import *

from adapters.GEN.questions_base import Questao

@app.messages.register_message_packs(routing_key="OpenAI.ChatCompletion.Sync", exchange_name="LLM_Requests")
class LLM_OpenAI_ChatCompletion_Sync(BaseMessagePack):
    ...

@app.messages.register_message_packs(routing_key="OpenAI.ChatCompletion.Async", exchange_name="LLM_Requests")
class LLM_OpenAI_ChatCompletion_Async(BaseMessagePack):
    ...
