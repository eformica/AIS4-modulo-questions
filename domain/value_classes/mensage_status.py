class Status:
    def __init__(self, mensage, code = None):
        self.mensage = mensage
        self.code = code

class StatusEnviado(Status):
    ...

class StatusProcessado(Status):
    ...

class StatusErro(Exception, Status):
    ...

