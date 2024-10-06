class RegistryDict(dict):
    def get_class_by_name(self, catalog, class_name):
        for k, v in self[catalog].items():
            if k.__name__ == class_name:
                return (k, v)
        raise Exception(f"Classe '{class_name}' não encontrada no catálogo '{catalog}'.")
    

X = RegistryDict()

X["teste"] = {RegistryDict: {"": ""}}

print(X.get_class_by_name("teste", "RegistryDict"))