import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from neomodel import (config
                      , db
                      ,  StructuredNode
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

class BaseNode(StructuredNode):
    __abstract_node__ = True

    uuid = UniqueIdProperty()
    uuid_user = StringProperty(index=True, required=True)
    create_at = DateTimeProperty(default_now=True)