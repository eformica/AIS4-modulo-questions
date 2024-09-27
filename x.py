
class MyClass:
    _decorated_functions = []

    def decorator(func):
        MyClass._decorated_functions.append(func.__name__)

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @decorator
    def function1(self):
        pass

    @decorator
    def function2(self):
        pass

    @classmethod
    def get_decorated_functions(cls):
        return cls._decorated_functions
    
print(MyClass.get_decorated_functions)

