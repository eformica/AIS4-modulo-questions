
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))


from abc import abstractmethod

from adapters.GEN.questions_base import Question
from adapters.messages_packs.LLM_messages_packs import *
from adapters.messages_packs.internal_messages_packs import *

from application.core.execution_controller import ExecutionController

from utils.decorator_catalog_builder_multi import decorator_factory
from domain.graph_models.questioners import NodeQuestioner, create_node_questioner
from adapters.GEN.questions_base import Question

from domain.value_classes.nodes_status import STATUS

# class StepOperator:
#     """Interface para a operação dos Steps (Questions ou outros objetos de retorno)."""

#     def __init__(self, obj):
#         self.obj = obj

#     def 
    
class QuestionerBase:
    add_step = decorator_factory("steps")

    def __init__(self):
        self._steps = __class__.add_step.to_list(self.__class__)
        
        self.uuid_node = None
        self._node = None

    @abstractmethod
    def start(self, objeto_exemplo, **kwargs) -> None:
        """Classe usada para instanciar os objetos pre-requisitos para o processamento.
        Exemplo:

        def start(self, projeto):
            self.projeto = projeto

        """

    def _register_node(self):

        #Status inicial dos steps:
        steps_status = []
        for k in self._steps:
            steps_status.append({"func": k.__name__, "status": STATUS.NOT_INITIALIZED.value})

        node_class = create_node_questioner("Questioner")

        self._node = node_class(
            uuid_user = self.uuid_user
            , class_name = self.__class__.__name__
            , steps_status = steps_status
            , questioner_status = 1
        )

        if self._node.save():
            self.uuid_node = self._node.uuid
        

    def _start_question(self, n_step: int, func_name: str, question: Question):
        request_node = question.start_request()
        
        if request_node:
            self._node.steps_status[n_step] = {"func": func_name, "status": STATUS.CREATED.value, "uuid_request": request_node.uuid}
            self._node.questions.connect(request_node, {"order": n_step, "func_name": func_name})
            self._node.save()

        else:
            raise Exception(f"Failed to create question request node. Step {n_step} [{func_name}].")

        if question.send_preposition_to_publisher():
            self._node.steps_status[n_step] = {"func": func_name, "status": STATUS.MESSAGE_SENT.value, "uuid_request": request_node.uuid}
            self._node.save()
        else:
            #TODO: atualizar status em caso de falha no envio da mensagem.
            ...
        
        return True
    
    def execute(self):

        if self._node is None:
            self._register_node()
        
        for n, item in enumerate(self._node.steps_status): #cada item de status steps é um dict com as chaves "status" e "func"
            if item["status"] == 0: #Node da pergunta nao criado
                if self._start_question(n, self._steps[n].__name__, self._steps[n](self)):
                    self._node.questioner_status = STATUS.PROCESSING.value
                    self._node.save()

                else:
                    self._node.questioner_status = STATUS.ERROR_GENERIC_FAILURE.value
                    self._node.save()

                break

            elif item["status"] == 9: #Step concluido
                continue

            elif (item["status"] < 9) and (item["status"] > 0): #Processando
                break

            elif (item["status"] >= 50) and (item["status"] < 60): #Falha no processo (realizar nova tentiva)
                #Tenta novamente:
                if self._start_question(n, self._steps[n].__name__, self._steps[n]()):
                    self._node.questioner_status = STATUS.PROCESSING.value
                    self._node.save()
                else:
                    self._node.questioner_status = STATUS.ERROR_GENERIC_FAILURE.value
                    self._node.save()
                break

            elif (item["status"] >= 90) and (item["status"] < 100): #Processo encerrado com erro terminal
                break

            else:
                Exception(f"Status code '{item["status"]}' not implanted.")



# class QuestionerActorBase:

#     #Metodos abstratos
    
#     @property
#     @abstractmethod
#     def input_object(self) -> object:
#         """Deve retornar o objeto de entrada, usado para instanciar a classe.""" 
    
#     @property
#     @abstractmethod
#     def core_object(self) -> Question:
#         """Deve retornar o objeto instanciado com a questao a ser formulada."""


# #--------------------------

#     def __init__(self):
#         self.EC = ExecutionController()

    
#     def _register_actor_node(self):
#         ...

#     def _register_response(self, response: dict):
#         ValuesClass = self.core_object.get_values_class()

#         obj = ValuesClass(**response)

#         self.EC.graph_db.create_node(obj)


#     #Implementacoes da classe herdada:
        
#     def on_trigged(self):
#         """
#         Executado quando um objeto de 'trigger_classes' é satisfeito, somente se todos os objetos de 'dependences' já
#         estiverem satisfeitos.
#         """
#         self.EC.address(self.core_object.preposition_to_publisher())

#     def on_message_received(self, message: BaseMessagePack):
#         """ 
#         Executado quando o objeto recebe uma mensagem diretamente.
#         O tipo da acao pode ser determinado por um condicional, avaliando o protocolo da mensagem (subclasse de BaseMessagePack).
#         """

#         if message.__class__ == Response_LLM_JSON:
#             ...
#         elif message.__class__ == Response_LLM_Text:
#             ...
#         elif message.__class__ == Response_LLM_Process_Status:
#             ...
#         else:
#             #Envia um status de erro internamente
#             ...

    
#     def on_dependence_satisfected(self, dependence_class):
#         """ 
#         Executado quando um objeto de 'dependences' comunica que foi satisfeito. Atualiza o status da relação de dependencias.
#         """

#     def on_processing(self):
#         """ 
#         Executado quando o objeto está em status on_processing. Deve atualizar o status do objeto.
#         """

#     def on_satisfected(self):
#         """ 
#         Executado quando o objeto é satisfeito. Deve atualizar o status do objeto.
#         """

#     def on_fail(self):
#         """ 
#         Executado quando o objeto falha em algum processo. Deve atualizar o status do objeto.
#         """