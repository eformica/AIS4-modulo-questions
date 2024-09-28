import functools
import inspect

class DecoratorListBuider:
    def __init__(self):
        self._dec_list = []

    def create_decorator(self, func):
        """Cria um decorator construtor para novos decorators"""

        #Define automaticamente o dicionario de propriedades: --------------------------------------------
        def _get_params(func):
            sig = inspect.signature(func)
            
            params = sig.parameters
            
            tem_args = any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in params.values())

            if tem_args:
                raise Exception("'*args' not allowed.")

            param_dict = {param.name: param.default if param.default is not inspect._empty else None for param in params.values()}

            return param_dict
        
        func_params = _get_params(func)

        if len(func_params) == 0: #Cria decorator simples

            func() #Executa o corpo da funcao quando o decorator é declarado.

            def decorator(func):
                self._dec_list.append(func)

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
                        if v == None:
                            propertys_to_register[k] = propertys_to_register_kwargs
                        else:
                            propertys_to_register[k] = v

                #-------------------------------------------------------------------------------

                def wrapper1(func2):
                    self._dec_list.append((func2, propertys_to_register))

                    @functools.wraps(func2)
                    def wrapper2(*args, **kwargs):
                        return func2(*args, **kwargs)
                    return wrapper2
                return wrapper1
        
        return decorator
    
    def get_list(self):
        return self._dec_list

        
if __name__ == "__main__":

    DLB = DecoratorListBuider()

    @DLB.create_decorator
    def decorator_com_parametros(a, b, c, d=3, **kwargs):
        """Decorator teste"""

        # Funcao transformada em um decorator de listagem. Os parametros definidos sao usados na definicão dos parametros que o
        # o decorator suporta.

        # Se possuir parametros, chamar:
        # @teste(1, b=2, c=3, d=4)
        # ==> É armazenado na lista uma tupla (funcao, {parametros})

        # Se nao possuir parametros, chamar apenas:
        # @teste
        # ==> Neste caso apenas a função decorada entra na lista.

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

    print(DLB.get_list())

    @DLB.create_decorator
    def decorator_sem_parametros():
        "Neste caso apenas a função decorada entra na lista."

    @decorator_sem_parametros
    def soma(a, b):
        return a + b
    
    print(DLB.get_list())

    print(soma(2, 3)) # A funcao decorada nao é afetada pelo decorador

    print(DLB.get_l
          ist()) # A execucao da funcao decorada nao altera em nada o objeto do DecoratorBuider