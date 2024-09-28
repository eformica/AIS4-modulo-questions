import functools
import inspect

class _ExecutionControllerList:

    def __init__(self) -> None:
        self._decorated = []


    def decorator(self
                  , trigger_class: object = None
                  , dependences: list[object] = None
                  , auto_process: bool = False):
        
        #Define automaticamente o dicionario de propriedades: --------------------------------------------
        def _get_params(func):
            sig = inspect.signature(func)
            
            params = sig.parameters
            param_dict = {param.name: param.default if param.default is not inspect._empty else None for param in params.values()}

            return param_dict

        properties = _get_params(self.decorator)

        for k, v in properties.items():
            properties[k] = eval(k)

        #---------------------------------------------------------------------------------

        def wrapper1(func):
            self._decorated.append((func, properties))

            @functools.wraps(func)
            def wrapper2(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper2
        return wrapper1
            
    def get_values(self):
        return self._decorated
    
class ExecutionController:
    def __init__(self) -> None:
        self.__execution_list = _ExecutionControllerList()
        self.add_item = self.__execution_list.decorator

    def get_list(self):
        return self.__execution_list.get_values()

EC = ExecutionController()


@EC.add_item()
class A:
    ...

@EC.add_item(trigger_class=A)
class B:
    ...

print(EC.get_list())