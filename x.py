import inspect

class BaseTeste:
    def f0(func):
        def wrapper(*args, **kwargs):
            print(func)
            return func(*args, **kwargs)
        return wrapper

class Teste(BaseTeste):
    x = 1
    
    @BaseTeste.f0
    def f1(self):
        ...

x = Teste()

import inspect

def get_class_name(func):
    for name, member in inspect.getmembers(func):
        print(name, member)
        if isinstance(member, type):
            return member.__name__
    return None

print(get_class_name(Teste.f1))