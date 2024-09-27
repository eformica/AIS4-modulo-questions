def create_dynamic_class(class_name, attributes, base=(object,)):
    """
    Cria uma classe dinamicamente com o nome especificado e os atributos fornecidos.

    Args:
        class_name (str): Nome da classe a ser criada.
        attributes (dict): Dicionário contendo os nomes dos atributos e seus valores iniciais.
        base (tuple): Tupla com a classe base da herança

    Returns:
        type: A nova classe criada.
    """

    attrs = {'__init__': lambda self, **kwargs: setattr(self, '__dict__', kwargs)}
    for attr_name, attr_value in attributes.items():
        attrs[attr_name] = attr_value
    return type(class_name, (object,), attrs)

teste = create_dynamic_class("Teste", {"nome": "Euclides"})

print(teste)