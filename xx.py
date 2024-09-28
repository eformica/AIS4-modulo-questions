import inspect

def teste(a, b=2, *args, **kwargs):

    def _get_params(func):
        sig = inspect.signature(func)
        
        params = sig.parameters
        param_dict = {param.name: param.default if param.default is not inspect._empty else None for param in params.values()}

        return param_dict

    param_dict = _get_params(teste)

    for k, v in param_dict.items():
        param_dict[k] = eval(k)

        print(param_dict)