import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from neomodel import (config
                      , db
                      , StructuredNode
                      , FulltextIndex
                      , VectorIndex
                      , UniqueIdProperty
                      , Relationship
                      , ArrayProperty
                      , BooleanProperty
                      , DateProperty
                      , DateTimeProperty
                      , FloatProperty
                      , IntegerProperty
                      , JSONProperty
                      , StringProperty)

from config import Settings
config.DATABASE_URL = Settings.NEO4J_URL

from domain.graph_models.base_node import BaseNode

class NodeQuestioner(BaseNode):
#    triggers = ArrayProperty()
#    dependences = ArrayProperty()

#    input_classes = ArrayProperty()
#    input_uuids = ArrayProperty()

    steps_status = ArrayProperty(required=True)

    questioner_status = IntegerProperty(required=True)

    report = JSONProperty()

#db.drop_constraints()
#db.drop_indexes()
#db.install_all_labels()