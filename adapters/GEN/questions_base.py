from application.app import app

from domain.ports.GEN import *
from domain.ports.mensages_packs_port import BaseMessagePack

import re
import inspect

def format_text(text):
    return re.sub(' {2,}', ' ', text).strip(' ')

def create_dynamic_class(class_name, attributes, base=(object,)):

    attrs = {'__init__': lambda self, **kwargs: setattr(self, '__dict__', kwargs)}
    
    for attr_name, attr_value in attributes.items():
        attrs[attr_name] = attr_value
    return type(class_name, (object,), attrs)

#--------------------------------------------------------------------------------------------

def datamodel_to_dynamic_class(class_name: str, data_model: dict, bases = (object,), ):
    attrs = {"__init__": ""}

    return type(class_name, bases, attrs)

class Especificacao_da_Resposta:
    def __init__(self, tipo: type = str, classe: object = None, observacoes: str = None, valores_possiveis: list = None, **kwargs):
        self.tipo = tipo
        self.classe = classe
        self.obsevacoes = observacoes
        self.valores_possiveis = valores_possiveis

        self.repr = tipo.__name__.title()

        if valores_possiveis is not None:
            self.repr += " valores_possiveis=" + str(valores_possiveis)

        if observacoes is not None:
            self.repr += " observacoes=" + str(observacoes)

        for k, v in kwargs.items():
            setattr(self, k, v)

            self.repr += " " + str(k) + "=" + str(v)

    def __repr__(self) -> str:
        return "<" + self.repr + ">"


class Tabela(BaseInfoModel):
    def __init__(self, data_model: dict) -> None:
        self.data_model = data_model

class Questao(BaseInfoModel):
    """
    data_model: modelo de dados usado para a geracao da pergunta/resposta
    origin_class: classe do objeto GEN de origem
    input_object: objeto de entrada para instanciação da classe de origem
    preposicao: pergunta a ser enviada
    respostas_multiplas: True -> a resposta retorna em list, False: a resposta retorna em dict
    agrupar: (Somente para respostas respostas_multiplas == True)
             True -> Registra o objeto de retorno em instancias separadas,
             False -> Registra o objeto de retorno na mesma instancia
    """
    def __init__(self
                 , data_model: dict
                 , origin_class: str
                 , input_object: object
                 , preposicao: str = None
                 , send_preposition_protocol: BaseMessagePack = None
                 , respostas_multiplas: bool = False
                 , agrupar: bool = True
                 ):
        
        self._data_model = data_model

        self._origin_class = origin_class
        self._input_object_class = input_object.__class__
        self._input_object_uuid = input_object.uuid

        self._respostas_multiplas = respostas_multiplas

        if preposicao is not None: 

            if respostas_multiplas == True:
                agrupar = True
                data_model_preposicao = {"resultados": [self._data_model, ]}
                self._preposicao = preposicao + f" Retorne o resultado em uma lista JSON conforme o seguinte modelo de dados: {data_model_preposicao}"
            else:
                self._preposicao = preposicao + f" Retorne o resultado em JSON conforme o seguinte modelo de dados: {self._data_model}"

        else:
            if not type(send_preposition_protocol) == BaseMessagePack:
                raise Exception("'send_preposition_protocol' must be a 'BaseMessagePack' type.")
        
        self._send_preposition_protocol = send_preposition_protocol

        self._agrupar = agrupar

    def send_preposition_to_publisher(self):
        if self._preposicao is None:
            raise Exception("'preposition' not defined.")
        
        message = self._send_preposition_protocol(origin_class = self._origin_class
            , input_object_class = self._input_object_class
            , input_object_uuid = self._input_object_uuid
            , content = self._preposicao
            )
        
        app.messages.publisher(message)


    def get_values_class(self):
        """Converte o data_model em uma nova classe adaptada para receber os valores do enriquecimento de dados e alimenta-los na base."""

        class_name = self.__class__.__name__ + "__Values"

        #o dict molde sera modificado para receber a estrutura de dados dos valores dos objetos
        molde = self._data_model.copy()

        def _tratamento_repositorio(obj):
            ...

        def _validacao_list(obj: list, chave: str):
            if len(obj) == 0:
                raise Exception(f"'Questao.data_model (dict)' suporta apenas listas com pelo menos um elemento da classe 'Especificacao_da_Resposta'. Chave '{chave}'")
            
            for j in obj:
                if not j.__class__ == Especificacao_da_Resposta:
                    raise Exception(f"Todos os items listas em 'Questao.data_model (dict)' devem ser da classe 'Especificacao_da_Resposta'. Chave '{chave}'")

        for k, v in molde.items():
            if v.__class__ == Repositorio:
                _tratamento_repositorio(v)

                molde[k] = "REPOSITORIO"

            elif (v.__class__ == list):
                molde[k] = "LISTA"

                _validacao_list(v)

            elif (v.__class__ == Especificacao_da_Resposta) and (v.tipo == list):
                raise Exception(f"Especificacao_da_Resposta não suporta o tipo 'list'. Utilize '[Especificacao_da_Resposta(...)]'. Chave '{k}'")
            
            elif (v.__class__ == Especificacao_da_Resposta):
                molde[k] = "Comum"

            else:
                raise Exception(f"'Questao.data_model (dict)' suporta apenas valores das classes 'list' ou 'Especificacao_da_Resposta'. Valor incopatível na chave '{k}'.")


        molde["_data_model"] = self._data_model #self.data_model é copiado para orientacao das regras de preenchimento

        print(molde)

        ValuesClass = create_dynamic_class(class_name, molde, (BaseValuesClass,))

        return ValuesClass
    
    def get_values(self, especific_fields: list|str|None = None):
        return "XXXXXXXXXXXXXXXX"

    def __repr__(self) -> str:
        return str(self.data_model)


class Repositorio:
    def __init__(self, base_model: BaseInfoModel):
        self.base_model = base_model

    def __repr__(self) -> str:
        return str(self.base_model.data_model)
