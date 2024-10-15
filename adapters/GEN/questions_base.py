from domain.ports.GEN import *
from domain.ports.mensages_packs_port import BaseMessagePack

from domain.graph_models.questions import QuestionRequest, QuestionResponse

import re

from datetime import date, datetime

def format_text(text):
    return re.sub(' {2,}', ' ', text).strip(' ')

#--------------------------------------------------------------------------------------------

class Especificacao_da_Resposta:

    def __init__(self
                 , tipo: type = str
                 , index: bool = False
                 , classe: object = None
                 , observacoes: str = None
                 , valores_possiveis: list = None
                 , **kwargs):
        
        self.tipo = tipo
        self.classe = classe
        self.obsevacoes = observacoes
        self.valores_possiveis = valores_possiveis
        self.index = index

        self.repr = tipo.__name__.title()

        if valores_possiveis is not None:
            self.repr += " valores_possiveis=" + str(valores_possiveis)

        if observacoes is not None:
            self.repr += " observacoes=" + str(observacoes)

        for k, v in kwargs.items():
            if k in ["index"]:
                continue

            setattr(self, k, v)

            self.repr += " " + str(k) + "=" + str(v)

    def __repr__(self) -> str:
        return "<" + self.repr + ">"


class Question(BaseInfoModel):
    """
    data_model: modelo de dados usado para a geracao da pergunta/resposta
    origin_class: classe do objeto GEN de origem
    input_object: objeto de entrada para instanciação da classe de origem
    preposition: pergunta a ser enviada
    respostas_multiplas: True -> a resposta retorna em list, False: a resposta retorna em dict
    agrupar: (Somente para respostas respostas_multiplas == True)
             True -> Registra o objeto de retorno em instancias separadas,
             False -> Registra o objeto de retorno na mesma instancia
    """

    def __init__(self
                 , title: str
                 , data_model: dict
                 , origin_class: str
                 , input_object: object
                 , preposition: str
                 , question_reason: str
                 , send_preposition_protocol: BaseMessagePack = None
                 , multiple_responses: bool = True
                 , group_in_the_same_node: bool = False
                 ):
        
        self.title = title

        self._data_model = data_model

        self._origin_class = origin_class
        
        self._input_object = input_object
        self._input_object_class = input_object.__class__
        self._input_object_uuid = input_object.uuid

        self.uuid_user = input_object.uuid_user

        self._multiple_responses = multiple_responses

        self._group_in_the_same_node = group_in_the_same_node

        self._question_reason = question_reason

        self._preposition = preposition

        self._prep_preposition()

        if not type(send_preposition_protocol) == BaseMessagePack:
            raise Exception("'send_preposition_protocol' must be a 'BaseMessagePack' type.")
        
        self._send_preposition_protocol = send_preposition_protocol

        self.uuid_request = None
        
        self._response_adapter = {"title": "title",
                                   "keywords": "keywords",
                                   "domain": "domain"}


    def config_response_adapter(self, title, keywords, domain):
        """Configura nomes diferentes para as variaveis esperadas no modelo de resposta."""

        self._response_adapter = {"title": title,
                                  "keywords": keywords,
                                  "domain": domain}

    def _prep_preposition(self):

        #TODO Adicoes no data_model:
        avaliacao_pergunta = {"Adequação da pergunta, dado o propósito da pergunta informado": Especificacao_da_Resposta(int, valores_possiveis=[
                                    "3: OK"
                                    , "2: Pergunta genérica, inespecífica ou pouco relevante"
                                    , "1: Pergunta inválida ou sarcástica"] )
                              , "Relevancia da pergunta": Especificacao_da_Resposta(int, valores_possiveis=[
                                    "3: Pergunta muito relevante para o objetivo"
                                    , "2: Pergunta de relevância média"
                                    , "1: Pergunta inválida ou irrelevante"])
                                }
        
        avaliacao_resposta = {"Relevância da resposta, dado o objetivo informado": Especificacao_da_Resposta(int, valores_possiveis=[
                                    "3: Relevância alta"
                                    , "2: Relevância média"
                                    , "2: Relevância baixa"] )
                              , "Confiança da resposta": Especificacao_da_Resposta(int, valores_possiveis=[
                                    "3: Alta"
                                    , "2: Média"
                                    , "1: Baixa"])
                                }
        
        #Adicoes na preposicao:

        self._preposition += " Considere o seguinte propósito da pergunta: " + self._question_reason

        if self._multiple_responses == True:
            data_model_preposicao = {"results": [self._data_model, ]}
            self._preposition += f" Retorne o resultado em uma lista JSON conforme o seguinte modelo de dados: {data_model_preposicao}"
        else:
            self._group_in_the_same_node = None
            self._preposition += f" Retorne o resultado em JSON conforme o seguinte modelo de dados: {self._data_model}"


    #---------------------------------------------------------------------------------------------------
    #Registra a pergunta

    def start_request(self):

        self._node_request = QuestionRequest(
            uuid_user = self.uuid_user
            , title = self.title
            , preposition = self._preposition

            , multiple_responses = self._multiple_responses
            , group_in_the_same_node = self._group_in_the_same_node

            , response_adapter = self._response_adapter
            , status = 0
            , send_method = str(self._send_preposition_protocol)
            , llm_model = None
            )
        
        if self._node_request.save():

            self.uuid_request = self._node_request.uuid

            return self._node_request.uuid
        
        else:
            return False
    
    #---------------------------------------------------------------------------------------------------
    #Envia a pergunta

    def send_preposition_to_publisher(self):
        
        if self.uuid_request is None:
            raise Exception("'uuid_request' not defined. Use method 'save_request' to get this.")
        
        self._data_model["uuid_user"] = self.uuid_user
        self._data_model["uuid_request"] = self.uuid_request

        message = self._send_preposition_protocol(origin_class = self._origin_class
            , input_object_class = self._input_object_class
            , input_object_uuid = self._input_object_uuid
            , content = self._preposition
            )
        
        from application.core.execution_controller import ExecutionController
        EC = ExecutionController()
        
        resp = EC.address(message)
        
        #Atualiza o status:
        #TODO: multiplas tentativas e tratamento da resposta do endereçamento

        self._node_request["status"] = 1 #Enviado (aguardando resposta)

        self._node_request.save()

        return message
    
    #---------------------------------------------------------------------------------------------------
    #Registra as respostas:

    @classmethod
    def _save_response_unit(cls
                            , uuid_request: str
                            , uuid_user: str
                            , response_unit: dict
                            , request_node: QuestionRequest|None = None):
        
        """Salva uma unidade de resposta."""

        if not request_node:
            request_node = QuestionRequest.nodes.get(uuid = uuid_request)

        #Registra propriedades de indice (title, keywords, domain):
        response_adapter = request_node.response_adapter

        props = {}
        for k, v in response_adapter.items():
            props[k] = response_unit[v]
            del response_unit[v]

        #Mantem apenas o conteudo da chave 'results' caso group_in_the_same_node == True:
        if ("results" in response_unit.keys()) and (request_node.group_in_the_same_node == True):
            response_unit = response_unit["results"]

        #Salva o node:
        response_node = QuestionResponse(
            uuid_user = uuid_user
            , content = response_unit
            , **props
        )

        response_node.save()

        request_node.question_response.connect(response_node)

        return response_node.uuid

    @classmethod
    def register_response_node(cls, response: dict):
        uuid_request = response["uuid_request"]
        uuid_user = response["uuid_user"]

        del response["uuid_request"], response["uuid_user"]

        request = QuestionRequest().nodes.get(uuid = uuid_request)

        if request.multiple_responses == True:
            if request.group_in_the_same_node == False:
                for ru in response["results"]:                    
                    cls._save_response_unit(uuid_request=uuid_request
                                        , uuid_user=uuid_user
                                        , response_unit=ru
                                        , request_node=request)
                    
            else: #group_in_the_same_node == True:
                resp_unit = {}
                for k, v in request.response_adapter.items():
                    resp_unit[v] = set()
                    for w in response["results"]:
                        if type(w[v]) == list:
                            resp_unit[v].update(w[v])
                        else:
                            resp_unit[v].add(w[v])

                resp_unit[v] = list(resp_unit[v])

                resp_unit["results"] = response["results"]

                cls._save_response_unit(uuid_request=uuid_request
                                        , uuid_user=uuid_user
                                        , response_unit=resp_unit
                                        , request_node=request)
                
        else: #multiple_responses == False:
            cls._save_response_unit(uuid_request=uuid_request
                                        , uuid_user=uuid_user
                                        , response_unit=response
                                        , request_node=request)
            
        #TODO: atualizar status do node
            
    #---------------------------------------------------------------------------------------------------
    
    def __repr__(self) -> str:
        return str(self._data_model)
