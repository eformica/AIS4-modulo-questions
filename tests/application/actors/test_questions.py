import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from adapters.GEN.questions_base import *
from adapters.messages_packs.LLM_messages_packs import Request_LLM_OpenAI_ChatCompletion_Sync
from application.Actors.questioners.questioners import Projeto
from domain.graph_models import *

import pytest

pr = Projeto(uuid_user="euclides"
             , uuid="projeto_teste"
             , tema="Criação de um sistema de inteligencia artificial auto-generativo"
             , objetivo="Testar"
             , especificacoes="Deverá ser usado o pytest")

#pr.save()

pr2 = Projeto().nodes.get(uuid="projeto_teste")


quest = Question(title="Ideação Inicial Agrupado"
        , data_model={"nome da ideia": Especificacao_da_Resposta(str)
                , "descrição": Especificacao_da_Resposta(str) 
                , "exposição do problema": Especificacao_da_Resposta(str)
                , "importancia": Especificacao_da_Resposta(str)
                , "tópicos para desenvolvimento": [Especificacao_da_Resposta(str, index=True)]
                , "palavras-chave para busca": [Especificacao_da_Resposta(str, index=True)]
                , "dominio": [Especificacao_da_Resposta(str, index=True)]
                , "abrangencia": [Especificacao_da_Resposta(str, index=True)]
                , "categoria do objetivo": Especificacao_da_Resposta(str, valores_possiveis=["Desenvolvimento de Negócio", "Desenvolvimento Tecnológico", "Trabalho Acadêmico"])
                }
                , origin_class=pr.__class__
                , input_object=pr
                , preposition=f"Dado o tema '{pr.tema}', proponha idéias para '{pr.objetivo}'. Considere as seguintes especificações: '{pr.especificacoes}'."
                , send_preposition_protocol=Request_LLM_OpenAI_ChatCompletion_Sync
                , multiple_responses=False
                , group_in_the_same_node=True
                )

quest.config_response_adapter(title="nome da ideia",
                              keywords="palavras-chave para busca",
                              domain="dominio")



request_uuid = quest.save_request("0")

# #request_uuid = "c65f3358183941f5abcfd9da80d31c5e"

print(request_uuid)

resposta = {
      'nome da ideia': "Ideia de teste", 
      'descrição': "", 
      'exposição do problema': "", 
      'importancia': "", 
      'tópicos para desenvolvimento': [""], 
      'palavras-chave para busca': ["mundo", "doido"], 
      'dominio': ["A", "B"], 
      'abrangencia': [""], 
      'categoria do objetivo': 'Desenvolvimento de Negócio'
      }
resposta2 = {
      'nome da ideia': "Segunda ideia", 
      'descrição': "", 
      'exposição do problema': "", 
      'importancia': "", 
      'tópicos para desenvolvimento': [""], 
      'palavras-chave para busca': ["sopa", "abóbora"], 
      'dominio': ["ddd"], 
      'abrangencia': [""], 
      'categoria do objetivo': 'Desenvolvimento de Negócio'
      }

resposta = {
    'uuid_user': "euclides",
    'uuid_request': request_uuid,
    'results': [
        resposta,
        resposta2
    ]
}


resposta_unitaria = {
      'uuid_user': "euclides",
      'uuid_request': request_uuid,
      'nome da ideia': "Resposta unitaria", 
      'descrição': "", 
      'exposição do problema': "", 
      'importancia': "", 
      'tópicos para desenvolvimento': [""], 
      'palavras-chave para busca': ["sopa", "abóbora"], 
      'dominio': ["ddd"], 
      'abrangencia': [""], 
      'categoria do objetivo': 'Desenvolvimento de Negócio'
      }

Question.register_response_node(resposta_unitaria)

#resp = QuestionResponse().nodes.get(uuid = response_uuid)
