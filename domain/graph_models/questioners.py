import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from neomodel import (config
                      , db
                      , StructuredNode
                      , StructuredRel
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

from domain.graph_models.questions import QuestionRequest

class RelQuestionStep(StructuredRel):
    order = IntegerProperty()
    func_name = StringProperty()

class NodeQuestioner(BaseNode):
#    triggers = ArrayProperty()
#    dependences = ArrayProperty()

#    input_classes = ArrayProperty()
#    input_uuids = ArrayProperty()

    __abstract_node__ = True

    class_name = StringProperty(required=True, index=True)

    steps_status = JSONProperty(required=True)

    questioner_status = IntegerProperty(required=True)

    report = JSONProperty()

    questions = Relationship(QuestionRequest, "QuestionStep", model=RelQuestionStep)

def create_node_questioner(class_name):
    res = type(class_name, (NodeQuestioner,), {})

    res.__optional_labels__ = ["Questioner"]

    return res

if __name__ == "__main__":
    db.drop_constraints()
    db.drop_indexes()
    db.install_all_labels()