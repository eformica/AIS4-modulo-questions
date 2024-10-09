import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from application.Actors.questioners.questioners import Projeto, Ideacao

from adapters.messages_packs.internal_messages_packs import Send_to_Next_Nodes

from application.core.execution_controller import ExecutionController

EC = ExecutionController()

pr = Projeto("Inteligencia Artificial para a resolução de grandes problemas da humanidade"
             , "Desenvolvimento de uma startup de tecnologia com a missão de facilitar e fomentar a criação de negócios inovadores"
             , """As principais linhas de negócio a serem abordadas são:
             Sustentabilidade Econômica e Ambiental
             , Desenvolvimento Social e Tecnológico
             , e Governança Coorporativa"""
             )

pr = Send_to_Next_Nodes(content=pr)

EC.address(pr)