from abc import ABC, abstractmethod

import re

def format_text(text):
    return re.sub(' {2,}', ' ', text).strip(' ')

#--------------------------------------------------------------------------------------------

def datamodel_to_dynamic_class(class_name: str, data_model: dict, bases = (object,), ):
    attrs = {"__init__": ""}

    return type(class_name, bases, attrs)

class Especificacao_da_Resposta:
    def __init__(self, tipo: str = "string", classe: object = None, observacoes: str = None, valores_possiveis: list = None, **kwargs):
        self.repr = "" 

        for k, v in kwargs.items():
            self.repr += str(k) + "=" + str(v) + ", "

    def __repr__(self) -> str:
        return "<" + self.repr + ">"

class BaseInfoModel:
    pass

class Tabela(BaseInfoModel):
    def __init__(self, data_model: dict) -> None:
        self.data_model = data_model

class Questao(BaseInfoModel):
    def __init__(self
                 , data_model: dict
                 , preposicao: str = None
                 , agrupar: bool = True
                 , **kwargs) -> None:
        
        self.data_model = data_model

        if preposicao is not None: 
            self.preposicao = preposicao + f" Retorne o resultado em JSON conforme o seguinte modelo de dados: {self.data_model}"

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __create_value_class(self):
        class_name = self.__class__.__name__ + "__Value"

        return create_dynamic_class(class_name, self.data_model)
    
    def get(self, campos: list|str|None = None):
        ...

    def __repr__(self) -> str:
        return str(self.data_model)

class Perguntar:
    def __init__(self
                 , base_question: Questao
                 , repetir=1) -> None:
        
        self.base_question = base_question
        self.repetir = repetir

    def __repr__(self) -> str:
        return str(self.base_question)

class Repositorio:
    def __init__(self, base_model: BaseInfoModel):
        self.base_model = base_model

    def __repr__(self) -> str:
        return str(self.base_model.data_model)


class QuestionBase(ABC):
    @property
    @abstractmethod
    def preposicao(self) -> str:
        ...

    @property
    @abstractmethod
    def data_model(self) -> dict[Especificacao_da_Resposta]:
        ...

    def to_class(self):
        class_name = self.__class__.__name__ + "__Value"

        return create_dynamic_class(class_name, self.data_model)