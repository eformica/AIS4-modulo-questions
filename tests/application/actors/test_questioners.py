import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from application.Actors.questioners.questioners import *

import pytest

pr = Projeto(id_usuario="euclides"
             , uid="projeto_teste"
             , tema="Criação de um sistema de inteligencia artificial auto-generativo"
             , objetivo="Testar"
             , especificacoes="Deverá ser usado o pytest")

ideacao = Ideacao(pr)

# print(ideacao.core_object.preposition_to_publisher().content)

# print(ideacao.core_object.get_values_class())

# resposta = {'resultados': [
#     {'nome da ideia': "", 
#      'descrição': "", 
#      'exposição do problema': "", 
#      'importancia': "", 
#      'tópicos para desenvolvimento': [""], 
#      'palavras-chave para busca': [""], 
#      'dominio': [""], 
#      'abrangencia': [""], 
#      'categoria do objetivo': 'Desenvolvimento de Negócio'
#      }
#      ]
#      }


# ideacao.on_trigged()