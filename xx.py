class SingletonWithID:
    _instances = {}
    _datalists = {}

    def __new__(cls, id, *args, **kwargs):
        if id not in cls._instances.keys():
            cls._instances[id] = super().__new__(cls)
            cls._datalists[id] = []
            cls._instances[id].__init__(id, *args, **kwargs)
        return cls._instances[id]

class Pessoa(SingletonWithID):

    def __init__(self, id, nome):
        self.nome = nome
        print(SingletonWithID._instances)

# Criando instâncias
p1 = Pessoa(1, "Alice")
p2 = Pessoa(1, "Bob")  # Retornará a instância p1
p3 = Pessoa(2, "Charlie")

print(p1 is p2)  # True, pois p2 é a mesma instância que p1
print(p1.nome, p2.nome)   # Alice
print(SingletonWithID._instances)