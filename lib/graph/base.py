
import json
import os
from datetime import datetime

from lib.aws.actions import ACTIONS
from lib.aws.resources import RESOURCES

from lib.graph.db import Neo4j


class Element:

    def __init__(self, properties={}, labels=[], key="Name"):

        if not isinstance(properties, dict):
            raise ValueError()

        if "Name" not in properties:
            raise ValueError("All elements must include a name")

        if key not in properties:
            raise ValueError("Missing key: '%s'" % key)

        self._properties = {}

        for k, v in properties.items():

            if any([isinstance(v, t) for t in [datetime, dict, list, int]]):
                self._properties[k] = v
                continue

            elif type(v) is None:
                self._properties[k] = ""
                continue

            try:
                self._properties[k] = json.loads(v)
                continue
            except json.decoder.JSONDecodeError:
                pass

            try:
                self._properties[k] = datetime.strptime(
                    v[:-6], '%Y-%m-%d %H:%M:%S')
                continue
            except ValueError:
                pass

            self._properties[k] = str(v)

        self._labels = set(labels)
        self._key = key

    def properties(self):
        return self._properties

    def label(self):
        return [l for l in self.labels()
                if l != self.__class__.__name__
                ][0]

    def labels(self):
        return sorted(list(self._labels))

    def type(self, label):
        return label in self._labels

    def id(self):
        return self._properties[self._key]

    def get(self, k):
        return self._properties[k]

    def set(self, k, v):
        self._properties[k] = v

    def __hash__(self):
        return hash(self.id())

    def __eq__(self, other):
        if isinstance(other, str):
            return other in self.labels()
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __gt__(self, other):
        return self.__hash__() > other.__hash__()

    def __repr__(self):
        return self.id()

    def __str__(self):
        return str(self.id())


class Node(Element):
    def __init__(self, properties={}, labels=[], key="Name"):
        super().__init__(properties, labels, key)


class Edge(Element):

    def __init__(self, properties={}, source=None, target=None, label=None):

        if label is None:
            label = [str(self.__class__.__name__).upper()]

        super().__init__(properties, label)

        self._source = source
        self._target = target
        self._set_id()

    def _set_id(self):

        self._id = hash("({source})-[:{label}{{{properties}}}]->({target})".format(
            source=self.source(),
            label=self.labels()[0],
            properties=json.dumps(self.properties(), sort_keys=True),
            target=self.target())
        )

    def source(self):
        return self._source

    def target(self):
        return self._target

    def id(self):
        return self._id

    def modify(self, k, v):
        super().set(k, v)
        self._set_id()

    def __str__(self):
        return str(self.get("Name"))


class Elements(set):

    def __init__(self, _=[], load=False, generics=False):

        super().__init__(_)

    def __add__(self, other):
        return Elements(self.union(other))

    def __iadd__(self, other):
        self.update(other)
        return Elements(self)

    def get(self, label):
        return Elements(filter(lambda r: r.type(label), self))

    def __repr__(self):
        return str([str(e) for e in self])
