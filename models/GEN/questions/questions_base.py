from abc import ABC, abstractmethod

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

class BaseInfoModel:
    pass

class Tabela(BaseInfoModel):
    def __init__(self, data_model: dict) -> None:
        self.data_model = data_model

class BaseValuesClass:
    def __init__(self) -> None:
        pass

class Questao(BaseInfoModel):
    def __init__(self
                 , data_model: dict
                 , origin_class: str
                 , input_object: object
                 , preposicao: str = None
                 , respostas_multiplas: bool = False
                 , agrupar: bool = True
                 , **kwargs) -> None:
        
        self._data_model = data_model

        self._origin_class_name = origin_class.__name__
        self._origin_class_src = inspect.getfile(origin_class)
        self._input_object_class_name = input_object.__class__.__name__
        self._input_object_class_src = inspect.getfile(input_object.__class__)
        self._input_object_uuid = input_object.uuid

        self._respostas_multiplas = respostas_multiplas

        if preposicao is not None: 

            if respostas_multiplas == True:
                agrupar = True
                data_model_preposicao = {"resultados": [self.data_model, ]}
                self._preposicao = preposicao + f" Retorne o resultado em uma lista JSON conforme o seguinte modelo de dados: {data_model_preposicao}"
            else:
                self._preposicao = preposicao + f" Retorne o resultado em JSON conforme o seguinte modelo de dados: {self.data_model}"

        self._agrupar = agrupar

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.ValuesClass = self.__datamodel_to_values_class()
    
    def get_question(self):
        question_packege = {"origin_class_name": self._origin_class_name
                            , "origin_class_src": self._origin_class_src
                            , "input_object_class_name": self._input_object_class_name
                            , "input_object_class_src": self._input_object_class_src
                            , "input_object_uuid": self._input_object_uuid
                            , "preposition": self._preposicao
                            }
        
        return question_packege
    
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
