import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from application.Actors.questioners.questioners import *

import pytest

pr = Projeto(uuid_user="euclides"
             , uuid="projeto_teste"
             , tema="Criação de um sistema de inteligencia artificial auto-generativo"
             , objetivo="Testar"
             , especificacoes="Deverá ser usado o pytest")

ideacao = Ideacao()
ideacao.start(uuid_user="euclides", projeto=pr)

ideacao.execute()