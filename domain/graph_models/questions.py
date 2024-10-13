import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2]))

from neomodel import (config
                      , db
                      ,  StructuredNode
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

class QuestionResponse(BaseNode):
    title = StringProperty(fulltext_index=FulltextIndex(), vector_index=VectorIndex())
    keywords = ArrayProperty(fulltext_index=FulltextIndex(), vector_index=VectorIndex())
    domain = ArrayProperty(fulltext_index=FulltextIndex(), vector_index=VectorIndex())
    content = JSONProperty()

class QuestionRequest(BaseNode):
    title = StringProperty(fulltext_index=FulltextIndex(), vector_index=VectorIndex())
    preposition = StringProperty()

    multiple_responses = BooleanProperty(required=True)
    group_in_the_same_node = BooleanProperty()
    response_adapter = JSONProperty(required=True)

    status = StringProperty(required=True)
    send_method = StringProperty(required=True)
    llm_model = StringProperty()

    question_response = Relationship(QuestionResponse, "Response")

#db.drop_constraints()
#db.drop_indexes()
#db.install_all_labels()