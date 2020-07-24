
import csv
import hashlib
import json
import os
import subprocess
import shutil
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

    def save(self, db="default.db", path="/opt/awspx/data"):

        edge_files = []
        node_files = []

        if not db.endswith(".db"):
            db = "%s.db" % db

        def stringify(s, t): return json.dumps(
            s, default=str) if t == "list" or t == "dict" else str(s)

        directory = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{db.split('.')[0]}"
        labels = sorted(list(set([
            next((l for l in e.labels()
                  if l not in ["External", "Generic", "Resource"]),
                 "Node")
            for e in self])))

        os.mkdir(f"{path}/{directory}")

        for label in labels:

            filename = "%s.csv" % label
            elements = self.get(label)

            if len(elements) == 0:
                continue

            header = sorted(list(set([
                (f, e.get(f).__class__.__name__)
                for e in elements for f in e.properties().keys()])))

            # We default to type: 'str' in cases where key names collide accross types

            header = list(set([
                (f, 'str' if [k for k, _ in header].count(f) > 1 else t)
                for (f, t) in header]))

            if type(next(iter(elements))) is Node or Node in type(next(iter(elements))).__bases__:

                prefix = [":ID"]
                suffix = [":LABEL"]
                data = [[e.id()] + [stringify(e.properties()[f], _)
                                    if f in e.properties()
                                    else '' for (f, _) in header]
                        + [";".join(e.labels())] for e in elements]

                node_files.append(filename)

            else:

                prefix = [":START_ID"]
                suffix = [":END_ID", ":TYPE"]

                data = [[e.source().id()] + [stringify(e.properties()[f], _)
                                             if f in e.properties()
                                             else '' for (f, _) in header]
                        + [e.target().id(), label] for e in elements if e.target() is not None]

                edge_files.append(filename)

            data.insert(0,
                        prefix + ["%s:%s" % (k, {
                            t:           t,
                            "NoneType": "string",
                            "dict":     "string",
                            "list":     "string",
                            "int":      "string",
                            "datetime": "string",
                            "bool":     "string",
                            "str":      "string"
                        }[t]) for (k, t) in header] + suffix)

            with open('%s/%s/%s' % (path, directory, filename), mode='w') as elements:

                c = csv.writer(
                    elements,
                    delimiter=',',
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)

                for row in data:
                    c.writerow(row)

        shutil.make_archive(f"{path}/{directory}",
                            'zip', f"{path}/{directory}")

        subprocess.Popen(["rm", "-rf", f"{path}/{directory}"])

        return f"{path}/{directory}.zip"

    def __repr__(self):
        return str([str(e) for e in self])
