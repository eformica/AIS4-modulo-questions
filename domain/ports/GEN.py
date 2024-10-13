from neomodel import UniqueIdProperty, StringProperty, StructuredNode

class BaseInfoModel:
    pass

class BaseValuesClass(StructuredNode):
    __abstract_node__ = True

    uid = UniqueIdProperty()
    user_id = StringProperty(index=True)
    project_id = StringProperty(index=True)
