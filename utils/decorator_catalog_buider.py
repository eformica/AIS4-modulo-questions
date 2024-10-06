import functools
import inspect

class SingletonWithID:
    _instances = {}
    _data = {}

    def __new__(cls, id, dict_class = dict, *args, **kwargs):
        if id not in cls._instances.keys():
            cls._instances[id] = super().__new__(cls)
            cls._data[id] = dict_class()
            cls._instances[id].__init__(id, *args, **kwargs)
        return cls._instances[id]
    
class DecoratorCatalogBuider(SingletonWithID):

    def __init__(self, id, enable_self_key_remover=True, dict_class: dict = dict):
        self.id = id
        self._data = SingletonWithID._data[id]
        
        if enable_self_key_remover:
            self.config_self_key_remover(True)
        else:
            self.config_self_key_remover(False)

    def config_self_key_remover(self, enable=True, key_name="self", key_position=0):
        """Criado para remover o elemento 'self' da primeira posicao dos parametros, caso o create_decorator seja usado dentro de uma classe."""

        self._selfkeyremover_enable = enable
        self._selfkeyremover_key_name = key_name
        self._selfkeyremover_key_position = key_position

    def _process_selfkeyremover(self, obj: dict):
        if self._selfkeyremover_enable == False:
            return obj
        
        if len(obj.keys()) < self._selfkeyremover_key_position:
            return obj
        
        if list(obj.keys())[self._selfkeyremover_key_position] == self._selfkeyremover_key_name:
            del obj[self._selfkeyremover_key_name]

        return obj
    
    def _tag_catalog_class(self, obj, catalog):
        obj._registry_catalog = catalog
        return obj

    def create_decorator(self, catalog: str):
        self._data[catalog] = {}

        def create_decorator_wrapper(func):
            """Cria um decorator construtor para novos decorators"""

            #Define automaticamente o dicionario de propriedades: --------------------------------------------
            def _get_params(func):
                sig = inspect.signature(func)
                
                params = sig.parameters
                
                tem_args = any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in params.values())

                if tem_args:
                    raise Exception("'*args' not allowed.")
                
                kwargs_params = [param.name for param in params.values() if param.kind == inspect.Parameter.VAR_KEYWORD]

                param_dict = {param.name: param.default if param.default is not inspect._empty else None for param in params.values()}

                return (param_dict, kwargs_params)
            
            func_params, kwargs_params = _get_params(func)

            if len(func_params) == 0: #Cria decorator simples

                func() #Executa o corpo da funcao quando o decorator é declarado.

                def decorator(func):
                    func = self._tag_catalog_class(func, catalog)

                    self._data[catalog][func] = {}

                    @functools.wraps(func)
                    def wrapper(*args, **kwargs):
                        return func(*args, **kwargs)
                    return wrapper
                
            else: #Cria decorator com parametros

                @functools.wraps(func)
                def decorator(*dec_args, **dec_kwargs):

                    func(*dec_args, **dec_kwargs) # A funcao é executada para validacao das propriedades

                    #Definicao dos parametros para registro: --------------------------------------------
                    propertys_to_register = {}
                    propertys_to_register_kwargs = {}

                    n = 0
                    for v in dec_args:
                        propertys_to_register[list(func_params.keys())[n]] = v
                        n += 1

                    for k, v in dec_kwargs.items():
                        if k not in func_params.keys():
                            propertys_to_register_kwargs[k] = v
                        else:
                            propertys_to_register[k] = v
                    
                    for k, v in func_params.items():
                        if k not in propertys_to_register.keys():
                            if k in kwargs_params:
                                propertys_to_register[k] = propertys_to_register_kwargs
                            else:
                                propertys_to_register[k] = v

                    #-------------------------------------------------------------------------------

                    propertys_to_register = self._process_selfkeyremover(propertys_to_register)

                    #-------------------------------------------------------------------------------
                    
                    def wrapper1(func2):
                        
                        func2 = self._tag_catalog_class(func2, catalog)

                        self._data[catalog][func2] = propertys_to_register

                        @functools.wraps(func2)
                        def wrapper2(*args, **kwargs):
                            return func2(*args, **kwargs)
                        return wrapper2
                    return wrapper1
            
            return decorator
        
        return create_decorator_wrapper
    
    def get_data(self) -> dict:
        return self._data

        
if __name__ == "__main__":
    class DictX(dict):
        ...

    DLB = DecoratorCatalogBuider("TESTE", dict_class=DictX)
    
    @DLB.create_decorator("catalog1")
    def decorator_com_parametros(a, b, c, d=3, **kwargs):
        """Decorator teste"""

        # Funcao transformada em um decorator de catalogação. Os parametros definidos sao usados na definicão dos parametros que o
        # o decorator suporta.

        # Se possuir parametros, chamar:
        # @teste(1, b=2, c=3, d=4)
        # ==> É armazenado uma chave no dict _data[funcao] = {parametros}

        # Se nao possuir parametros, chamar apenas:
        # @teste
        # ==> Neste caso o valor armazenado é um dict vazio

        # **kwargs pode ser usados como parametro:
        # def teste(a, **kwargs)
        # @teste(a=1, x=100, y=200, z=1000) ===> OK

        # *args NAO DEVE SER USADO:
        # def teste(*args)
        # @teste(1, 2, 3) =====> RETORNA ERRO

        # Podem ser atribuidos valores padrao na chamada da função
        # def teste(a=1) ===> OK

        # O corpo da funcao decorada por 'create_decorator' é executado somente quando o decorator é declarado sobre
        # outra funcao. Isso é util para documentação e validação dos parametros do decorator.


    @decorator_com_parametros(1, 2, d=4, c=3, z="vai para kwargs")
    def xxx(a, b, c):
        ...


    print(DLB.get_data())

    @DLB.create_decorator("catalog2")
    def decorator_sem_parametros():
        "Neste caso apenas a função decorada entra na lista."

    @decorator_sem_parametros
    def soma(a, b):
        return a + b
    
    print(DLB.get_data())

    print(soma(2, 3)) # A funcao decorada nao é afetada pelo decorador

    print(DLB.get_data()) # A execucao da funcao decorada nao altera em nada o objeto do DecoratorBuider

    print(soma.__dict__)