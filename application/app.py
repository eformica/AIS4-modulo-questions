import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[1]))

import subprocess, logging

from application.core.registry import RegistryController, get_registry

registry = RegistryController()

def _start_listeners(registry):
    """Inicia todos os listeners registrados."""

    listeners_process = []

    for k, v in registry["listeners"].items():
        logging.warning(f"Iniciando listener '{k.__name__}':")

        listeners_process.append(subprocess.Popen(['python'
                                                        , 'application/listener_runner.py'
                                                        , k.__name__]
                                                        , start_new_session=False))
    return listeners_process

#--------------------------------------------------------------------

#Registra os modulos do App:

if __name__ == "__main__":
    logging.warning(f"Registrando módulos da aplicacao:")

    from application.Actors.questioners.questioners import *
    from adapters.messages_packs.internal_messages_packs import *
    from application.listeners.listener2 import Listener2
    from application.listeners.listener1 import Listener1

    registry.save()

    registry = get_registry()

    logging.warning(f"{registry}")

    #---------------------------------------------
            
    #Inicia os listeners:

    listeners_process = _start_listeners(registry)

    print(listeners_process)