import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[3]))

from application.app import app

from adapters.messages.messages_packs import *
from adapters.GEN.questions_base import Especificacao_da_Resposta, Questao, Repositorio, Tabela, format_text

TopicosParaDesenvolvimento = Repositorio({"nome do topico": Especificacao_da_Resposta(str)
                                       , "categoria": Especificacao_da_Resposta(str, valores_possiveis=[""])
                                       })

PalavrasChave = Repositorio({"palavra-chave": Especificacao_da_Resposta(str)
                            , "categoria": Especificacao_da_Resposta(str, valores_possiveis=[""])
                            })

class Espec_PalavrasChave:
    ...

class Espec_Dominio:
    ...

class Espec_Abrangencia:
    ...

@app.add_to_execution_list()
class Projeto:
    def __init__(self, tema: str, objetivo: str, especificacoes: str = None, uuid: int|None = None):
        self.uuid = uuid
        self.tema = tema
        self.objetivo = objetivo
        self.especificacoes = especificacoes
        
        self.enrich_data_models = {}

@app.add_to_execution_list(trigger_class=Projeto)
class Ideacao:
    def __init__(self
                 , projeto: Projeto):
        
        self.projeto = projeto

    @property
    def input_object(self):
        return self.projeto 
    
    @property
    def question(self):
        preposicao = f"Dado o tema '{self.projeto.tema}', proponha idéias para '{self.projeto.objetivo}'."

        if self.projeto.especificacoes is not None:
            preposicao += f" Considere as seguintes especificações: '{self.projeto.especificacoes}'."

        question = Questao(
                {"nome da ideia": Especificacao_da_Resposta(str)
                , "descrição": Especificacao_da_Resposta(str) 
                , "exposição do problema": Especificacao_da_Resposta(str)
                , "importancia": Especificacao_da_Resposta(str)
                , "tópicos para desenvolvimento": TopicosParaDesenvolvimento
                , "palavras-chave para busca": [Especificacao_da_Resposta(str, classe=Espec_PalavrasChave)]
                , "dominio": [Especificacao_da_Resposta(str)]
                , "abrangencia": [Especificacao_da_Resposta(str)]
                , "categoria do objetivo": Especificacao_da_Resposta(str, valores_possiveis=["Desenvolvimento de Negócio", "Desenvolvimento Tecnológico", "Trabalho Acadêmico"])
                }
                , origin_class=__class__
                , input_object=self.input_object
                , preposicao=preposicao
                , send_preposition_protocol=LLM_OpenAI_ChatCompletion_Sync
                , respostas_multiplas = True
                , agrupar=False
                )
        
        return question

    def register_response(self, response):
        ValuesClass = self.question.get_values_class()

        Obj = ValuesClass(response)

        repo = Repositorio() #...

#        Obj.add_repo(repo)

#        Obj.insert_all_and_commit()


#print(app._execution_list)
    



# proj = Projeto("Tema1", "Objetivo grandioso")

# X = Ideacao(proj)

# items = X.controller.items

# print(items)
# print("______________________________________________________________________________")

# print(items["IdeacaoInicial"]())
# print("______________________________________________________________________________")

# print(items["AnalisePublicoAlvo"]().content)
# print("______________________________________________________________________________")

# #print(items["AnalisePublicoAlvo"]().content.preposicao)

# print(X.controller.send_item("AnalisePublicoAlvo"))



class PublicoAlvo:

    def _PublicoAlvo(self):
        preposicao = f"""Dado o tema '{self.tema}' e o objetivo '{self.objetivo}', avalie a ideia '{
            self.controller.get_values("IdeacaoInicial", ["nome da ideia",
                                                        "descrição",
                                                        "exposição do problema",
                                                        "importancia"
                                                        ])}' quanto ao seu 'publico-alvo'."""
        
        AnalisePublicoAlvo = Questao({"nome da persona": Especificacao_da_Resposta(str)
                                        , "tipo": Especificacao_da_Resposta(str, valores_possiveis=["Pessoa Física", "Pessoa Jurídica"])
                                        , "sexo": Especificacao_da_Resposta(str, valores_possiveis=["Masculino", "Feminino"])
                                        , "faixa-etaria": Especificacao_da_Resposta(str, valores_possiveis=["0-14", "15-29", "30-44", "45-60", "+60"], unidade="anos")
                                        , "escolaridade": Especificacao_da_Resposta(str, valores_possiveis=[""])
                                        , "porte": Especificacao_da_Resposta(str, valores_possiveis=[""])
                                        , "área de atuação": Especificacao_da_Resposta(str, valores_possiveis=[""])
                                        , "áreas de interesses": [Especificacao_da_Resposta(str, valores_possiveis=[""])]
                                        , "dores e oportunidades": [Especificacao_da_Resposta(str)]
                                        , "outras especifícações": Especificacao_da_Resposta(str)
                                        }
                                        , respostas_multiplas=True
                                        , preposicao=preposicao
                                        )
        
        return LLM_OpenAI_ChatCompletion_Sync(AnalisePublicoAlvo)


    def _AnaliseConcorrencia(self):
        
        preposicao = f"""Dado o tema '{self.tema}' e o objetivo '{self.objetivo}', avalie a ideia '{
            self.controller.get_values("IdeacaoInicial", ["nome da ideia",
                                                        "descrição",
                                                        "exposição do problema",
                                                        "importancia"
                                                        ])}' quanto ao seus 'concorrentes'."""
        
        AnaliseConcorrencia = Questao({"nome do concorrente": Especificacao_da_Resposta(str)
                                        , "categoria": Especificacao_da_Resposta(str, valores_possiveis=[""])
                                        }
                                        , respostas_multiplas=True
                                        , preposicao=preposicao
                                        )
        
        return LLM_OpenAI_ChatCompletion_Sync(AnaliseConcorrencia)
    

    def _AnaliseDiferenciais(self):
        preposicao = f"""Dado o tema '{self.tema}' e o objetivo '{self.objetivo}', avalie a ideia '{
            self.controller.get_values("IdeacaoInicial", ["nome da ideia",
                                                        "descrição",
                                                        "exposição do problema",
                                                        "importancia"
                                                        ])}' quanto ao seu 'diferenciais'."""
        
        Diferenciais = Questao({"nome do diferencial": Especificacao_da_Resposta(str)
                    , "categoria": Especificacao_da_Resposta(str, valores_possiveis=[""])
                    }
                    , respostas_multiplas=True
                    , preposicao=preposicao)
        
        return LLM_OpenAI_ChatCompletion_Sync(Diferenciais)

        #     data_model = {"geral": Perguntar(Ideia),
        #     "diferenciais": [Perguntar(Diferenciais, 3)],
        #     "análise da concorrência": [Perguntar(AnaliseConcorrencia, 5)],
        #     "análise do público alvo": Perguntar(AnalisePublicoAlvo, 1)
        #     }
    
        # self.enrich_data_models["ideacao"] = Questao(data_model=data_model, preposicao=preposicao)











# class GEN__ParametrosEIndicadores1(QuestionBase):
#     """Gera parâmetros e indicadores objetivos a partir de um assunto, tema e objetivo (opcional)."""
#     def __init__(self
#                  , assunto: str
#                  , tema: str
#                  , bool_assunto_especifico: bool
#                  , objetivo: str = ""
#                  , parent_tema: str = None
#                  ):

#         self.assunto = assunto
#         self.tema = tema
#         self.bool_assunto_especifico = bool

#         if bool_assunto_especifico:
#             self.especificidade_assunto = "especificamente a"
#         else:
#             self.especificidade_assunto = "a qualquer"

#         if objetivo ==  "":
#             self.objetivo = "" 
#         else:
#             self.objetivo = f"com o objetivo '{objetivo}'"

#     @property
#     def preposicao(self):
#         return format_text(f"""
#             Gere uma lista completa indicadores ou atributos que podem ser aplicados {self.especificidade_assunto} {self.assunto}, 
#             considerando o tema "{self.tema}" {self.objetivo}. Retorne apenas o resultado em JSON, sem qualquer outro dado adicional,
#             conforme o seguinte modelo de dados: {self.data_model}""")
    
#     @property
#     def data_model(self):
#         return {"nome do indicador ou atributo": Especificacao_da_Resposta(str),
#             "tipo indicador": Especificacao_da_Resposta(str, valores_possiveis=['numero inteiro', 'numero decimal', 'classificação categórica' , 'atributo lista discreta de itens']),
#             "unidade de medida": Especificacao_da_Resposta(str),
#             "tipo da fonte de dados": Especificacao_da_Resposta(str, valores_possiveis=["Dados Públicos", "Medição Direta", "Dados Privados"]),
#             "serie historica": Especificacao_da_Resposta(bool, observacoes="apenas para itens numericos que possuam alteracao de valores no tempo"),
#             "dominio": Especificacao_da_Resposta(list, classe=Espec_Dominio, observacoes="lista completa de valores possiveis, apenas para classificação categórica)"),
#             "abrangencia": Especificacao_da_Resposta(list, classe=Espec_Abrangencia, observacoes="nivel de abrangencia ao qual o indicador é aplicado"),
#             "palavras-chave para busca": Especificacao_da_Resposta(list, classe=Espec_PalavrasChave),
#             "adimite detalhamento": Especificacao_da_Resposta(bool),
#             "exemplos de detalhamento": Especificacao_da_Resposta(str, observacoes="lista de novos indicadores que poderiam ser trazidos para detalhar a informação"),
#             "descrição": Especificacao_da_Resposta(str),
#             "fórmula ou método de estimativa": Especificacao_da_Resposta(str)
#             }

# X = GEN__ParametrosEIndicadores1("X", "Y", True)

# print(X.to_class())
# Dados o tema ou pergunta 'OPORTUNIDADES DE INVESTIMENTO' no contexto de qualquer 'ATIVIDADE ECONOMICA', objetivando 'NOVOS MODELOS DE NEGÓCIOS SUSTENTÁVEIS E INOVADORES', elenque perguntas relevantes, retornando o resultado em JSON conforme o seguinte modelo de dados:
# ["pergunta": str,
# "importancia da pergunta": str,
# "tópicos esperados na resposta": list, 
# "palavras-chave para busca": list,
# "adimite detalhamento": bool,
# "exemplos de detalhamento": str,
# "dominio": list,
# "abrangencia": list
# ]

# Dados o tema ou pergunta 'Sensoriamento Remoto para Predição de Volume e Produtividade Florestal' no contexto de qualquer 'ATIVIDADE ECONOMICA', objetivando 'NOVOS MODELOS DE NEGÓCIOS SUSTENTÁVEIS E INOVADORES', elenque perguntas relevantes, retornando o resultado em JSON conforme o seguinte modelo de dados:
# ["pergunta": str,
# "importancia da pergunta": str,
# "tópicos esperados na resposta": list, 
# "palavras-chave para busca": list,
# "adimite detalhamento": bool,
# "exemplos de detalhamento": str,
# "dominio": list,
# "abrangencia": list
# ]


# Dados o tema 'Sensoriamento Remoto para Predição de Volume e Produtividade Florestal' proponha idéias para 'modelos de negócios sustentáveis e inovadores', retornando o resultado em JSON conforme o seguinte modelo de dados:
# ["nome da ideia": str,
# "resumo": str, 
# "problema de negócio": str,
# "importancia da solução": str,
# "possíveis diferenciais": str,
# "análise da concorrência": str,
# "principais concorrentes diretos": list,
# "público alvo": list,
# "tópicos para desenvolvimento": list, 
# "palavras-chave para busca": list,
# "dominio": list,
# "abrangencia": list
# ]
