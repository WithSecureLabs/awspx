from lib.graph.base import Edge, json


class Associative(Edge):

    def __init__(self,  properties={}, source=None, target=None):
        super().__init__(properties, source, target)


class Transitive(Edge):

    def __init__(self,  properties={}, source=None, target=None):
        super().__init__(properties, source, target)


class Action(Edge):

    def __init__(self,  properties={}, source=None, target=None):

        for key in ["Name", "Description", "Effect", "Access", "Reference", "Condition"]:
            if key not in properties:
                raise ValueError("Edge properties must include '%s'" % key)

        super().__init__(properties, source, target)


class Trusts(Action):

    def __init__(self,  properties={}, source=None, target=None):

        super().__init__(properties, source, target)
