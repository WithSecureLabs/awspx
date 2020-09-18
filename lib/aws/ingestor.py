import boto3
import csv
import json
import os
import re
import shutil
import sys
import subprocess
import zlib
from base64 import b64decode
from datetime import datetime

from botocore.exceptions import (ClientError,
                                 PartialCredentialsError, ProfileNotFound)

from lib.aws.actions import ACTIONS
from lib.aws.policy import (BucketACL, IdentityBasedPolicy,
                            ObjectACL, ResourceBasedPolicy)

from lib.aws.resources import RESOURCES
from lib.graph.base import Elements, Node
from lib.graph.edges import (Action, Associative,
                             Transitive, Trusts)

from lib.graph.nodes import Generic, Resource


class IngestionManager(Elements):

    zip = None

    def __init__(self, session, console=None,
                 services=[], db="default.db",
                 quick=False, skip_actions=False,
                 only_types=[], skip_types=[],
                 only_arns=[], skip_arns=[]):

        try:

            if console is None:
                from lib.util.console import console
            self.console = console

            identity = self.console.task(
                "Awaiting response to sts:GetCallerIdentity",
                session.client('sts').get_caller_identity,
                done=lambda r: '\n'.join([
                    f"Identity: {r['Arn']}",
                    f"Services: {', '.join([s.__name__ for s in services])}",
                    f"Database: {db}",
                    f"Account:  {r['Account']}",
                    f"Region:   {session.region_name}",
                ]))

            self.account = identity["Account"]
            self.console.spacer()

        except (ClientError, PartialCredentialsError, ProfileNotFound) as e:
            self.console.error(str(e))
            sys.exit(1)

        if len(only_arns) > 0:
            only_types = list(set(only_types + [RESOURCES.label(arn)
                                                for arn in only_arns]))

        for ingestor in services:

            elements = ingestor(session=session, console=self.console,
                                account=self.account, quick=quick,
                                only_types=only_types, skip_types=skip_types,
                                only_arns=only_arns, skip_arns=skip_arns)

            super().update(elements)
            elements.destroy()

        self.load_transitives()

        if not skip_actions:
            self.load_actions()

        self.zip = self.save(db)

        self.console.spacer()

    def load_transitives(self):

        resources = self.get("Resource")
        groups = resources.get("AWS::Iam::Group")
        roles = resources.get("AWS::Iam::Role")
        policies = resources.get("AWS::Iam::Policy")
        instance_profiles = resources.get("AWS::Iam::InstanceProfile")

        for resource in self.console.tasklist(
            "Adding Transitive relationships",
            iterables=resources,
            done="Added Transitive relationships",
        ):

            if resource.label() in ["AWS::Iam::User", "AWS::Iam::Group", "AWS::Iam::Role"]:

                # (User|Group|Role) --> (Policy)
                if "AttachedManagedPolicies" in resource.properties():

                    policy_arns = [policy["PolicyArn"]
                                   for policy in resource.get("AttachedManagedPolicies")]

                    for policy in filter(lambda r: r.id() in policy_arns,
                                         policies):

                        self.add(Transitive(properties={"Name": "Attached"},
                                            source=resource, target=policy))

                        policy_arns = [p for p in policy_arns
                                       if p != str(policy)]

                    if not len(policy_arns) > 0:
                        del resource.properties()["AttachedManagedPolicies"]

                # (User)-->(Group)
                if (resource.label() in ["AWS::Iam::User"]
                        and "GroupList" in resource.properties()):

                    group_names = resource.get("GroupList")

                    for group in filter(
                            lambda r: r.get("Name") in group_names,
                            groups):

                        self.add(Transitive(properties={"Name": "Attached"},
                                            source=resource, target=group))

                        group_names = [g for g in group_names
                                       if g != str(group)]

                    if not len(group_names) > 0:
                        del resource.properties()["GroupList"]

            # (Instance) --> (Instance Profile)
            if (resource.label() in ["AWS::Ec2::Instance"]
                    and "IamInstanceProfile" in resource.properties()):

                instance_profile = next((i for i in instance_profiles
                                         if str(i) == resource.get("IamInstanceProfile")["Arn"]
                                         ), None)

                if instance_profile is not None:

                    self.add(Transitive({"Name": "Attached"},
                                        source=resource, target=instance_profile))

                    del resource.properties()["IamInstanceProfile"]

            # (InstanceProfile) --> (Role)
            if (resource.label() in ["AWS::Iam::InstanceProfile"]
                    and "Roles" in resource.properties()):

                role_arns = list(map(lambda r: r["Arn"],
                                     resource.get("Roles")))

                for role in filter(
                        lambda r: r.id() in role_arns,
                        roles):

                    self.add(Transitive(properties={"Name": "Attached"},
                                        source=resource, target=role))

                    role_arns = [r for r in role_arns if r != str(role)]

                if not len(role_arns) > 0:
                    del resource.properties()["Roles"]

            # (Function) --> (Role)
            if (resource.label() in ["AWS::Lambda::Function"]
                    and "Role" in resource.properties()):

                role = next((r for r in roles
                             if str(r) == resource.get("Role")
                             ), None)

                if role is not None:

                    self.add(Transitive(properties={"Name": "Attached"},
                                        source=resource, target=role))

                    del resource.properties()["Role"]

    def load_actions(self):

        self.add(Node(labels=["CatchAll"], properties={
            "Name": "CatchAll",
            "Description": "A sinkhole for actions affecting unknown resource types."
        }))

        # Resource types Actions affect
        resources = Elements(e for e in self if any([l in [
            "Resource", "Generic", "CatchAll"
        ] for l in e.labels()]))

        # IAM entities
        entities = Elements(e for e in self.get("Resource")
                            if e.label() in ['AWS::Iam::User', 'AWS::Iam::Role'])

        for resource in self.console.tasklist(
            "Resolving Policy information",
            iterables=self.get("Resource"),
            done="Added Action relationships"

        ):

            # Identity-based policies (inline and managed)
            if resource.label() in [
                "AWS::Iam::User",  "AWS::Iam::Group", "AWS::Iam::Role",
                "AWS::Iam::Policy"
            ]:

                self.update(IdentityBasedPolicy(
                    resource, resources).actions())

            # Resource-based policies
            if resource.label() in [
                "AWS::S3::Bucket", "AWS::S3::Object",
            ]:
                resource_based_policy = ResourceBasedPolicy(
                    resource=resource, resources=resources,
                    keys="Policy")

                self.update(resource_based_policy.principals())
                self.update(resource_based_policy.actions())

            # Assume role policy documents
            if resource.label() in ["AWS::Iam::Role"]:

                resource_based_policy = ResourceBasedPolicy(
                    resource=resource,
                    resources=resources,
                    keys="Trusts"
                )

                # Skip AWS::Domain principals
                self.update(Elements(principal
                                     for principal in resource_based_policy.principals()
                                     if not principal.type("AWS::Domain")))

                # Only actions beginning with sts:AssumeRole are valid
                for action in [action for action in resource_based_policy.actions()
                               if str(action).startswith("sts:AssumeRole")]:

                    # This role trusts all IAM entities within this account
                    if (action.source().type("AWS::Account")
                            and action.source().id().split(':')[4] == self.account):

                        self.update(Elements(Trusts(properties=action.properties(),
                                                    source=action.target(),
                                                    target=entity)
                                             for entity in entities))

                    else:
                        # Skip AWS::Domain actions
                        if action.source().type("AWS::Domain"):
                            continue

                        self.add(action)
                        self.add(Trusts(properties=action.properties(),
                                        source=action.target(),
                                        target=action.source()))

            # ACLs (bucket & objects)
            if resource.label() in ["AWS::S3::Bucket", "AWS::S3::Object"]:

                acl = BucketACL(resource, resources) \
                    if resource.label() == "AWS::S3::Bucket" \
                    else ObjectACL(resource, resources)

                self.update(acl.principals())
                self.update(acl.actions())

    def save(self, db="default.db", path="/opt/awspx/data"):

        archive = None
        edge_files = []
        node_files = []

        if not db.endswith(".db"):
            db = "%s.db" % db

        directory = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{db.split('.')[0]}"
        labels = sorted(list(set([
            next((l for l in e.labels()
                  if l not in ["External", "Generic", "Resource"]),
                 "Node")
            for e in self])))

        os.mkdir(f"{path}/{directory}")

        def stringify(s, t):
            return json.dumps(s, default=str) \
                if t == "list" or t == "dict" \
                else str(s)

        for label in self.console.tasklist(
            "Saving ingested data",
            labels,
            done=f"Saved ingested data to {directory}.zip"
        ):

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
                data = [[e.id()] + [stringify(e.get(f), _)
                                    if f in e.properties()
                                    else '' for (f, _) in header]
                        + [";".join(e.labels())] for e in elements]

                node_files.append(filename)

            else:

                prefix = [":START_ID"]
                suffix = [":END_ID", ":TYPE"]

                data = [[e.source().id()] + [stringify(e.get(f), _)
                                             if f in e.properties()
                                             else '' for (f, _) in header]
                        + [e.target().id(), label] for e in elements if e.target() is not None]

                edge_files.append(filename)

            data.insert(0, prefix + [
                "%s:%s" % (k, {
                    t:           t,
                    "NoneType": "string",
                    "dict":     "string",
                    "list":     "string",
                    "int":      "string",
                    "datetime": "string",
                    "bool":     "string",
                    "str":      "string"
                }[t]) for (k, t) in header] + suffix)

            with open(f"{path}/{directory}/{filename}", mode='w') as elements:

                c = csv.writer(
                    elements,
                    delimiter=',',
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)

                for row in data:
                    c.writerow(row)

            if label == labels[-1]:

                shutil.make_archive(f"{path}/{directory}",
                                    'zip', f"{path}/{directory}")

                subprocess.Popen(["rm", "-rf", f"{path}/{directory}"])

                archive = f"{path}/{directory}.zip"

        return archive

    def update(self, elements):

        for element in elements:
            self.add(element)

    def add(self, element):

        length = len(self)
        super().add(element)

        if len(self) == length:
            return

        if "TRANSITIVE" in element.labels():

            self.console.info(f"Added {element.label().capitalize()} relationship: "
                              f"({element.source()}) → ({element.target()})")

        elif any([e in ["ACTION", "TRUSTS"] for e in element.labels()]):
            pass

        else:
            self.console.info(f"Added {element.label()}: ({element})")


class SessionClientWrapper(object):

    codes = [
        'AccessDenied',
        'AccessDeniedException',
    ]

    def __init__(self, client, console=None):

        self.client = client
        self.console = console

    def __iter__(self):
        try:
            for i in self.client.__iter__():
                yield i
        except ClientError as e:
            if e.response['Error']['Code'] in self.codes:
                self.console.warn(str(e))
                yield {}
            else:
                raise e

    def __getattr__(self, attr):

        method = self.client.__getattribute__(attr)

        if callable(method):

            def hook(*args, **kwargs):

                result = {}

                try:
                    result = method(*args, **kwargs)

                    if attr in ['get_paginator', 'paginate']:
                        result = self.__class__(result, console=self.console)

                except ClientError as e:

                    if e.response['Error']['Code'] in self.codes:
                        self.console.warn(str(e))
                    else:
                        raise e

                return result

            return hook

        else:
            return method


class Ingestor(Elements):

    types = []
    associations = []

    _only_types = []
    _skip_types = []
    _only_arns = []
    _skip_arns = []

    def __init__(self, session, account, console,
                 load_resources=True, quick=False,
                 only_types=[], skip_types=[],
                 only_arns=[], skip_arns=[]):

        self.console = console.item(f"Ingesting {self.__class__.__name__}")
        self.session = session
        self.account = account
        self.quick = quick

        self._only_arns = only_arns
        self._skip_arns = skip_arns

        if self.__class__.__name__.lower() not in self.session.get_available_services():
            self.console.critical(f"'{self.__class__.__name__}' is not a recognized boto service.\n"
                                  f"Only the following services are supported: {', '.join(self.session.get_available_services())}.")

        if (load_resources and self.__class__.__name__.lower() not in self.session.get_available_resources()):
            self.console.critical(f"'{self.__class__.__name__}' is not a supported boto resource. "
                                  "This means you'll need to write a custom ingestor (see Lambda for a practical example).\n"
                                  f"Only the following services are supported: {', '.join(self.session.get_available_resources())}.")

        self.client = SessionClientWrapper(self.session.client(
            self.__class__.__name__.lower()),
            console=self.console)

        # If no resources to ingest have been specified, assume all
        if len(self.types) == 0:
            self.types = [t for t in RESOURCES
                          if t.startswith(f"AWS::{self.__class__.__name__}::")]

        # There must be nothing specified for this service
        if len(self.types) == 0:
            self.console.critical(f"No AWS::{self.__class__.__name__} resources were found in 'lib.aws.resources.py'. "
                                  "You'll need to add them before this ingestor will work.")
            return

        # Ensure ingested resources conform to RESOURCES casing
        self.types = [r for r in map(lambda r: next(
            (t for t in RESOURCES if t.upper() == r.upper()), None), self.types)
            if r is not None]

        # Remove types that dont match user specifications
        self.types = [t for t in self.types if t not in skip_types
                      and (len(only_types) == 0 or t in only_types)]

        self.load_generics()

        if load_resources and len(self.types) > 0:
            self.load_resources()
            self.load_associatives()

    def load_generics(self, types=None):

        for k in self.console.tasklist(
            f"Adding Generic resources",
            self.types,
            done=f"Added Generic resources"
        ):
            self.add(Generic(properties={
                "Name": f"${k.split(':')[-1]}",
                "Arn":  RESOURCES.definition(k),
            }, labels=[k]))

    def load_resources(self):

        def get_resource_type_model(collection):

            service = self.__class__.__name__.capitalize()
            resource_model = collection.meta.resource_model._resource_defs
            remap = {k: f"AWS::{service}::{v}"
                     for k, v in {k: resource_model[k]["shape"]
                                  if "shape" in resource_model[k]
                                  and not resource_model[k]["shape"].startswith("Get")
                                  else k for k in resource_model.keys()
                                  }.items()}

            # Map model types to RESOURCE definitions
            for k, v in list(remap.items()):

                if "load" in resource_model[k]:

                    operation = resource_model[k]["load"]["request"]["operation"]

                    # Find other resource types produced by the same operation.
                    options = sorted([rt for rt, o in {
                        rt: resource_model[key]["load"]["request"]["operation"]
                        for key, rt in remap.items() if "load" in resource_model[key]}.items()
                        if o == operation], key=lambda x: x in RESOURCES, reverse=True)

                    if options[0] in RESOURCES:
                        remap[k] = options[0]
                        continue

                # Find other resource types that have the same identifiers.
                for alias in [rt for rt, i in {key: json.dumps(
                    resource_model[key]["identifiers"], sort_keys=True)
                        for key in resource_model.keys()}.items()
                        if i == json.dumps(resource_model[k]["identifiers"], sort_keys=True)]:

                    if f"AWS::{service}::{alias}" in RESOURCES:
                        remap[k] = f"AWS::{service}::{alias}"
                        break

            model = {k: {remap[getattr(collection, k)._model.resource.type]: {}}
                     for k in [attr for attr in dir(collection)
                               if boto3.resources.collection.CollectionManager
                               in getattr(collection, attr).__class__.__bases__]
                     }

            # Update model to include reflect resources which themselves
            # are CollectionManager(s).
            for rt in resource_model.keys():

                for rm in boto3.resources.factory.ResourceModel(
                        rt, resource_model[rt],
                        resource_model).collections:

                    # Explicitly skip Version objects
                    if rm._definition["resource"]["type"].endswith("Version"):
                        continue

                    # Remap model key (only once)
                    if rt in remap:
                        rt = remap[rt]

                    resource_type = remap[rm._definition["resource"]["type"]]
                    operation = rm.name

                    # Skip this operation if another method producing this resource
                    # type is available from the root collection
                    if resource_type in [list(i.keys())[0]
                                         for i in model.values()]:
                        continue

                    for k, v in model.items():

                        if rt in v.keys():
                            v[rt][operation] = {resource_type: {}}
                            break

            return model

        def run_ingestor(collections, model):

            if not len(collections) > 0:
                return

            for attr, v in model.items():

                label = list(v.keys())[0]
                collection_managers = []

                if len(self.types) > 0 and label not in self.types:

                    collateral = [
                        rt for rt in [list(k.keys())[0] for k in list(v.values())[0].values()]
                        if rt in self.types
                        and rt not in [list(k.keys())[0] for k in model.values()]
                    ]

                    self.console.debug(''.join((
                        f"Skipped {label} ingestion ",
                        f"({', '.join(collateral)} will also be skipped)." if len(collateral) > 0 else "")))

                    continue

                rt = ''.join(''.join([f" {c}" if c.isupper() else c for c in getattr(
                    collections[0], attr)._model.request.operation]).split()[1:])

                for operation, collection in self.console.tasklist(
                    f"Adding {rt}",
                    iterables=map(lambda c: (
                        getattr(c, attr).all, c), collections),
                    wait=f"Awaiting response to {self.__class__.__name__.lower()}:"
                    f"{getattr(collections[0], attr)._model.request.operation}",
                    done=f"Added {rt}"
                ):

                    for cm in SessionClientWrapper(operation(), console=self.console):

                        collection_managers.append(cm)

                        if 'meta' not in dir(cm) or cm.meta.data is None:

                            self.console.warn(f"Skipping ServiceResource {cm}: "
                                              "it has no properties")
                            continue

                        cm.meta.data["Name"] = [getattr(cm, i)
                                                for i in cm.meta.identifiers
                                                ][-1] if "Name" not in cm.meta.data.keys() \
                            else cm.meta.data["Name"]

                        properties = {
                            **cm.meta.data,
                            **dict(collection.meta.data
                                   if collection is not None
                                   and not collection.__class__.__name__.endswith("ServiceResource")
                                   and collection.meta.data is not None
                                   else {}),
                        }

                        try:
                            cm.meta.data["Arn"] = RESOURCES.definition(label).format(
                                Region=self.session.region_name,
                                Account=self.account,
                                **properties)

                        except KeyError as p:

                            self.console.warn(f"Failed to construct resource ARN: defintion for type '{label}' is malformed - "
                                              f"boto collection '{cm.__class__.__name__}' does not have property {p}, "
                                              f"maybe you meant one of the following ({', '.join(properties.keys())}) instead?")
                            continue

                        # Add Resource
                        resource = Resource(labels=[label],
                                            properties=cm.meta.data)
                        self.add(resource)

                for _, attrs in v.items():
                    run_ingestor(collection_managers, attrs)

        service = self.__class__.__name__.lower()
        collection = self.session.resource(service)
        model = get_resource_type_model(collection)

        run_ingestor([collection], model)

    def load_associatives(self):

        if len(self.associations) == 0:
            return

        def set_references(references, item, key=None):

            if isinstance(item, list):
                [set_references(references, i) for i in item]

            elif isinstance(item, dict):
                [set_references(references, v, k) for k, v in item.items()]

            elif (key is not None
                  and any([isinstance(item, t) for t in [str, int, bool]])
                  and len(str(item)) > 0):

                if key not in references:
                    references[key] = set()

                references[key].update([item])

        for resource in self.console.tasklist(
            f"Adding Associative relationships",
            self.get("Resource"),
            done="Added Associative relationships"
        ):

            # Extract reference key-value pairs from this resource's
            # properties (if we need to)
            prop_refs = {}

            # Extract reference key-value pairs from this resource's ARN:
            regex = re.compile(RESOURCES[resource.label()])
            matches = regex.match(resource.id())
            arn_refs = {k: set([matches.group(k)])
                        for k in regex.groupindex.keys()
                        } if matches is not None else {}

            # For each of the resource types associated with this resource type
            for rt in [[rt for rt in association if rt != resource.label()][0]
                       for association in self.associations
                       if resource.label() in association]:

                refs = {}
                required = list(re.compile(RESOURCES[rt]).groupindex.keys())

                # We have all the information we need using just the ARN
                if all([k in arn_refs for k in required]):
                    refs = arn_refs
                else:
                    # Check the resource's properties (once)
                    if len(prop_refs) == 0:
                        set_references(prop_refs,
                                       resource.properties())

                    # Use property and ARN refs (ARN values take precedence)
                    refs = {
                        **{k: v for k, v in prop_refs.items()
                           if k in required},
                        **{k: v for k, v in arn_refs.items()
                           if k in required},
                    }

                    # There isn't enough information to create a reference ARN
                    if not all([k in refs for k in required]):
                        continue

                # Hopefully, this never happens
                if not all([len(v) == 1 for v in refs.values()]):
                    continue

                # Construct a reference ARN and get the associated resource
                arn = RESOURCES.types[rt].format(
                    **{k: list(v)[0] for k, v in refs.items()})

                associate = next((r for r in self
                                  if r.id() == arn), None)

                if associate is None:
                    # self.console.debug(f"Couldn't create association: resource ({arn}), "
                    #                    f"referenced by {resource}, doesn't exist ")
                    continue

                (source, target) = sorted((resource, associate),
                                          key=lambda r: r.id())

                self.add(Associative(properties={"Name": "Attached"},
                                     source=source, target=target))

    def update(self, elements):
        for element in elements:
            self.add(element)

    def add(self, element):

        if any(r in element.labels() for r in ["Resource", "Generic"]):

            if element.label() not in self.types:
                self.console.debug(f"Skipping {element}: "
                                   f"type ({element.label()}) does not match user specifications")
                return

            if "Resource" in element.labels() and \
                ((len(self._only_arns) > 0 and element.id() not in self._only_arns)
                 or (len(self._skip_arns) > 0 and element.id() in self._skip_arns)):
                self.console.debug(f"Skipping {element}: "
                                   "ARN does not match user specifications")
                return

        length = len(self)
        super().add(element)

        if len(self) == length:
            return

        elif "Resource" in element.labels():
            self.console.info(
                f"Added {element.label().split(':')[-1]} ({element})")
        elif "Generic" in element.labels():
            self.console.info(
                f"Added Generic {element.label().split(':')[-1]} ({element})")

        elif any([e in ["ASSOCIATIVE", "TRANSITIVE"] for e in element.labels()]):
            self.console.info(f"Added {element.label().capitalize()} relationship: "
                              f"({element.source()}) → ({element.target()})")

    def destroy(self):
        associatives = len(self.get("ASSOCIATIVE"))
        resources = len(self.get("Resource"))
        generics = len(self.get("Generic"))

        self.console.notice(f"Added {resources} Resource(s), {generics} Generic(s), "
                            f"and {associatives} Associative relationship(s)")
        del self


class IAM(Ingestor):

    types = [
        "AWS::Iam::User", "AWS::Iam::Role", "AWS::Iam::Group",
        "AWS::Iam::Policy", "AWS::Iam::InstanceProfile",
        "AWS::Iam::MfaDevice", "AWS::Iam::VirtualMfaDevice"
    ]

    associations = [
        ("AWS::Iam::User", "AWS::Iam::VirtualMfaDevice")
    ]

    def __init__(self, *args, **kwargs):

        super().__init__(**kwargs, load_resources=False)

        self.get_account_authorization_details()
        self.load_associatives()

        if not self.quick:
            self.list_user_mfa_devices()
            self.get_login_profile()
            self.list_access_keys()

    def get_account_authorization_details(self):

        resources = [str(f"{t}s" if t != "Policy" else "Policies")
                     for t in [t.split(':')[-1] for t in self.types]
                     if t in ["User", "Group", "Role", "Policy", "InstanceProfile"]]

        if not len(resources) > 0:
            return

        elif len(resources) > 1:
            resources[-1] = f"and {resources[-1]}"

        resources = ', '.join(resources)

        def get_aad_resources(item, label):

            resources = []
            properties = {}

            for k in sorted(item.keys()):

                 # Rename PolicyLists to Documents
                if k.endswith("PolicyList"):
                    properties["Documents"] = [{
                        p["PolicyName"]: p["PolicyDocument"]
                        for p in item[k]}]

                # Rename AssumeRolePolicyDocument to Trusts
                elif k == "AssumeRolePolicyDocument":
                    properties["Trusts"] = item[k]

                # Add instance profiles
                elif k == "InstanceProfileList":
                    [resources.extend(get_aad_resources(instance_profile, "InstanceProfile"))
                     for instance_profile in item[k]]

                # Rename PolicyVersionList to Document
                elif k == "PolicyVersionList":

                    properties["Document"] = [{
                        "DefaultVersion": [p for p in item[k] if p["IsDefaultVersion"]
                                           ][0]["Document"]
                    }]

                # Remove label from property key
                elif label in k:
                    properties[k.replace(label, "")] = item[k]

                # No change
                else:
                    properties[k] = item[k]

            # Add Resource
            resources.append(Resource(
                labels=[f"AWS::Iam::{label}"],
                properties=properties))

            return resources

        for page in self.console.tasklist(
            f"Adding {resources}",
            iterables=self.client.get_paginator(
                "get_account_authorization_details").paginate(),
            wait="Awaiting response to iam:GetAccountAuthorizationDetails",
            done=f"Added {resources}"
        ):

            account_authorization_details = [
                (k.replace("DetailList", "").replace("Policies", "Policy"), detail)
                for k, v in page.items() if isinstance(v, list)
                for detail in v]

            for label, item in account_authorization_details:
                for resource in get_aad_resources(item, label):
                    self.add(resource)

    def get_login_profile(self):

        for user in self.console.tasklist(
                "Updating User login profile information",
                iterables=self.get("AWS::Iam::User").get("Resource"),
                done="Updated User login profile information"
        ):

            try:
                login_profile = self.client.get_login_profile(
                    UserName=user.get("Name"))["LoginProfile"]
                del login_profile["UserName"]
                user.set("LoginProfile", login_profile)
                self.console.info(
                    f"Updated User ({user}) login profile information")

            except self.client.exceptions.NoSuchEntityException:
                pass

    def list_access_keys(self):

        for user in self.console.tasklist(
            "Updating User access key information",
            iterables=self.get("AWS::Iam::User").get("Resource"),
            done="Updated User access key information",
        ):

            try:
                access_keys = self.client.list_access_keys(
                    UserName=user.get("Name"))[
                    "AccessKeyMetadata"]

                for i in range(len(access_keys)):
                    k = access_keys[i]["AccessKeyId"]
                    del access_keys[i]["AccessKeyId"]
                    del access_keys[i]["UserName"]
                    access_keys[i] = {
                        k: access_keys[i]
                    }

                user.set("AccessKeys", access_keys)
                self.console.info(
                    f"Updated User ({user}) access key information")

            except self.client.exceptions.NoSuchEntityException:
                pass

    def list_user_mfa_devices(self):

        if not any([r in self.types for r in [
            "AWS::Iam::MfaDevice",
            "AWS::Iam::VirtualMfaDevice"
        ]]):
            return

        for user in self.console.tasklist(
                "Adding MfaDevices",
                iterables=self.get("AWS::Iam::User").get("Resource"),
                wait="Awaiting response to iam:ListMFADevices",
                done="Added MFA devices",
        ):

            for mfa_device in self.client.list_mfa_devices(
                UserName=user.get("Name")
            )["MFADevices"]:

                label = RESOURCES.label(mfa_device["SerialNumber"])
                mfa_device["Arn"] = mfa_device["SerialNumber"]
                mfa_device["Name"] = mfa_device["Arn"].split('/')[-1] if label == "AWS::Iam::MfaDevice" \
                    else "Virtual Device" if label == "AWS::Iam::VirtualMfaDevice" \
                    else "Device"

                if label is None:
                    continue

                del mfa_device["SerialNumber"]

                resource = Resource(
                    labels=[label],
                    properties=mfa_device
                )

                self.add(resource)


class EC2(Ingestor):

    types = [
        'AWS::Ec2::DhcpOptions',
        # 'AWS::Ec2::Image',
        'AWS::Ec2::Instance',
        'AWS::Ec2::InternetGateway',
        'AWS::Ec2::KeyPair',
        'AWS::Ec2::NetworkAcl',
        'AWS::Ec2::NetworkInterface',
        'AWS::Ec2::PlacementGroup',
        'AWS::Ec2::RouteTable',
        'AWS::Ec2::SecurityGroup',
        # 'AWS::Ec2::Snapshot',
        'AWS::Ec2::Subnet',
        'AWS::Ec2::Volume',
        'AWS::Ec2::Vpc',
        'AWS::Ec2::VpcPeeringConnection',
    ]

    associations = [
        ("AWS::Ec2::Instance", "AWS::Ec2::NetworkInterface"),
        ("AWS::Ec2::Instance", "AWS::Ec2::KeyPair"),
        ("AWS::Ec2::Instance", "AWS::Ec2::Volume"),
        ("AWS::Ec2::NetworkInterface", "AWS::Ec2::SecurityGroup"),
        ("AWS::Ec2::NetworkInterface", "AWS::Ec2::Subnet"),
        ("AWS::Ec2::Vpc", "AWS::Ec2::VpcPeeringConnection"),
        ("AWS::Ec2::Vpc", "AWS::Ec2::InternetGateway"),
        ("AWS::Ec2::Vpc", "AWS::Ec2::DhcpOptions"),
        ("AWS::Ec2::Vpc", "AWS::Ec2::RouteTable"),
        ("AWS::Ec2::Vpc", "AWS::Ec2::NetworkAcl"),
        ("AWS::Ec2::Vpc", "AWS::Ec2::Subnet"),
    ]

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if not self.quick:
            self.get_instance_user_data()

    def get_instance_user_data(self):

        for instance in self.console.tasklist(
            "Updating Instance user data information",
            iterables=self.get("AWS::Ec2::Instance").get("Resource"),
            wait="Awaiting response to ec2:DescribeInstanceAttribute",
            done="Updated Instance user data information"
        ):

            name = instance.get("Name")

            try:
                response = self.client.describe_instance_attribute(Attribute="userData",
                                                                   DryRun=False,
                                                                   InstanceId=name)
            except ClientError as e:
                self.console.error(f"Couldn't get user data for {name} "
                                   "- it may no longer exist.")

            if 'UserData' in response.keys() and 'Value' in response['UserData'].keys():
                userdata = b64decode(response['UserData']['Value'])
                if userdata[0: 2] == b'\x1f\x8b':  # it's gzip data
                    userdata = zlib.decompress(
                        userdata, zlib.MAX_WBITS | 32).decode('utf-8')
                else:  # normal b64
                    userdata = userdata.decode('utf-8')

                instance.set("UserData", {"UserData": userdata})
                self.console.info(f"Updated Instance ({instance}) user data")


class S3(Ingestor):

    types = [
        'AWS::S3::Bucket',
        'AWS::S3::Object',
    ]

    associations = [
        ('AWS::S3::Bucket', 'AWS::S3::Object')
    ]

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if not self.quick:
            self.get_bucket_policies()
            self.get_bucket_acls()
            self.get_public_access_blocks()
            self.get_object_acls()

    def get_bucket_policies(self):

        for bucket in self.console.tasklist(
            "Updating Bucket policy information",
            iterables=self.get("AWS::S3::Bucket").get("Resource"),
            wait="Awaiting response to s3:GetBucketPolicy",
            done="Updated Bucket policy information"
        ):

            try:
                policy = self.client.get_bucket_policy(
                    Bucket=bucket.get('Name'))["Policy"]

                bucket.set("Policy", json.loads(policy))
                self.console.info(f"Updated Bucket ({bucket}) policy")

            except (ClientError, KeyError) as e:
                self.console.warn("Failed to update "
                                  f"Bucket policy ({bucket}). "
                                  f"{e if isinstance(e, ClientError) else ''}")

    def get_public_access_blocks(self):

        for bucket in self.console.tasklist(
            "Updating Bucket public access block information",
            iterables=self.get("AWS::S3::Bucket").get("Resource"),
            wait="Awaiting response to s3:GetPublicAccessBlock",
            done="Updated Bucket public access block information"
        ):

            # https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html
            # Implicitly affects Bucket ACLs and Policies (values returned by associated get requests
            # specify what is being enforced rather than actual values)

            try:
                public_access_block = self.client.get_public_access_block(
                    Bucket=bucket.get("Name")
                )["PublicAccessBlockConfiguration"]

                bucket.set("PublicAccessBlock", public_access_block)
                self.console.info(f"Updated Bucket ({bucket}) "
                                  "public access block")

            except (ClientError, KeyError) as e:
                self.console.warn("Failed to update Bucket "
                                  f"public access block ({bucket}). "
                                  f"{e if isinstance(e, ClientError) else ''}")

    def get_bucket_acls(self):

        for bucket in self.console.tasklist(
            "Updating Bucket ACL information",
            iterables=self.get("AWS::S3::Bucket").get("Resource"),
            wait="Awaiting response to s3:GetBucketACL",
            done="Updated Bucket ACL information",
        ):
            try:
                acl = self.client.get_bucket_acl(Bucket=bucket.get('Name'))
                bucket.set("ACL", {
                    "Owner": acl["Owner"],
                    "Grants": acl["Grants"]
                })
                self.console.info(f"Updated Bucket ({bucket}) ACL")

            except (ClientError, KeyError) as e:
                self.console.warn("Failed to update "
                                  f"Bucket ACL ({bucket}). "
                                  f"{e if isinstance(e, ClientError) else ''}")

    def get_object_acls(self):

        for obj in self.console.tasklist(
            "Updating Object ACL information",
            iterables=self.get("AWS::S3::Object").get("Resource"),
            wait="Awaiting response to s3:GetObjectACL",
            done="Updated Object ACL information"
        ):
            try:
                arn = obj.get("Arn")
                bucket, *key = arn.split(':::')[1].split('/')
                key = "/".join(key)

                acl = self.client.get_object_acl(Bucket=bucket, Key=key)
                obj.set("ACL", {
                    "Owner": acl["Owner"],
                    "Grants": acl["Grants"]
                })
                self.console.info(f"Updated Object ({obj}) ACL")

            except (ClientError, KeyError) as e:
                self.console.warn("Failed to update "
                                  f"Object ACL ({obj}). "
                                  f"{e if isinstance(e, ClientError) else ''}")


class Lambda(Ingestor):

    types = [
        'AWS::Lambda::Function',
    ]

    def __init__(self, *args, **kwargs):

        super().__init__(**kwargs, load_resources=False)

        self.list_functions()

    def list_functions(self):

        if 'AWS::Lambda::Function' not in self.types:
            return

        functions = Elements()

        for function in [f for r in self.console.tasklist(
            "Adding Functions",
            iterables=self.client.get_paginator("list_functions").paginate(),
            wait="Awaiting response to lambda:ListFunctions",
            done="Added Functions"
        ) for f in r["Functions"]]:

            function["Name"] = function["FunctionName"]
            function["Arn"] = function["FunctionArn"]
            del function["FunctionName"]
            del function["FunctionArn"]

            function = Resource(
                properties=function,
                labels=["AWS::Lambda::Function"])

            self.add(function)
