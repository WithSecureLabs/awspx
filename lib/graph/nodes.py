from lib.graph.base import Node


class Generic(Node):

    def __init__(self, properties={}, labels=[]):

        label = self.__class__.__name__

        super().__init__(properties,
                         labels + [label] if label not in labels else labels,
                         "Arn")


class Resource(Node):

    def __init__(self, properties={}, labels=[], key="Arn"):

        label = self.__class__.__name__

        super().__init__(properties,
                         labels + [label] if label not in labels else labels,
                         key)

    def account(self):
        if "Arn" not in self.properties() or len(self.properties()["Arn"].split(':')) < 5:
            return None

        return str(self.properties()["Arn"].split(':')[4])


class External(Node):

    def __init__(self, properties={}, labels=[], key="Name"):

        label = self.__class__.__name__

        super().__init__(properties,
                         labels + [label] if label not in labels else labels,
                         key)
