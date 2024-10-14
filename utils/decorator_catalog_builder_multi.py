import functools

def decorator_factory(id):
    class DecoratorCls:
        __mark_id = id
        
        @staticmethod
        def __call__(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            setattr(wrapper, "_mark_id", __class__.__mark_id)
            
            return wrapper
        
        def to_list(self, cls):
            res = []
            for k in dir(cls):

                if "_mark_id" in dir(eval(f'cls.{k}')):
                    if eval(f'cls.{k}._mark_id') == __class__.__mark_id:
                        res.append((k, eval(f'cls.{k}')))

            return res
        
    obj = DecoratorCls()

    return obj

if __name__ == "__main__":
    
    #Exemplo de uso:

    class TesteBase:
        add_step = decorator_factory("steps")
        add_X = decorator_factory("X")

        def __init__(self):
            self._steps = __class__.add_step.to_list(self.__class__)
            self._X = __class__.add_X.to_list(self.__class__)

    class A(TesteBase):
        @TesteBase.add_step
        def f1(self):
            ...

        @TesteBase.add_step
        def f2(self):
            ...

        @TesteBase.add_X
        def f3(self):
            ...

    class B(TesteBase):
        @TesteBase.add_step
        def w1(self):
            ...

        @TesteBase.add_step
        def w2(self):
            ...

        @TesteBase.add_X
        def w3(self):
            ...

    testeA = A()

    testeB = B()

    print("Steps de A: ", testeA._steps)
    print("X de A: ", testeA._X)
    print("Steps de B: ", testeB._steps)
    print("X de B: ", testeB._X)
