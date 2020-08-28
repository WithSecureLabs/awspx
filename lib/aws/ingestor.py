import copy
import json
import re
import sys
import zlib
from base64 import b64decode
from functools import reduce

import boto3
from botocore.exceptions import ClientError
from lib.aws.actions import ACTIONS
from lib.aws.policy import BucketACL, ObjectACL, IdentityBasedPolicy, ResourceBasedPolicy
from lib.aws.resources import RESOURCES
from lib.graph.base import Elements, Node
from lib.graph.db import Neo4j
from lib.graph.edges import Action, Associative, Transitive, Trusts
from lib.graph.nodes import Generic, Resource


class Ingestor(Elements):

    types = []
    associations = []

    _only_types = []
    _skip_types = []
    _only_arns = []
    _skip_arns = []

    def __init__(self, session, account="000000000000", default=True, verbose=True, quick=False,
                 only_types=[], skip_types=[], only_arns=[], skip_arns=[]):

        self.session = session
        self.account = account
        self._verbose = verbose

        self._only_arns = only_arns
        self._skip_arns = skip_arns

        if default:
            available_resources = self.session.get_available_resources()
            if self.__class__.__name__.lower() not in available_resources:
                self._print(f"[-] '{self.__class__.__name__}' is not a supported boto resource. "
                            "This means you'll need to write a custom ingestor (see Lambda for a practical example). "
                            f"For future reference, boto supports: {', '.join(available_resources)}.")
                return

        # If no resources to ingest have been specified, assume all
        if len(self.types) == 0:
            self.types = [t for t in RESOURCES if t.upper().startswith(
                "AWS::%s::" % self.__class__.__name__.upper())]

        # There must be nothing specified for this service
        if len(self.types) == 0:
            self._print(f"[-] No {self.__class__.__name__.capitalize()} resources were found in 'lib.aws.resources.py'. "
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

        print("[*] Commencing {resources} ingestion\n".format(
            ingestor=self.__class__.__name__,
            resources=', '.join([
                r if (i == 0 or i % 3 > 0)
                else f'\n{" " * 15}{r}'
                for i, r in enumerate(self.types)])
        ))

        if default and len(self.types) > 0:
            self.load_resources()
            self.load_associatives()

    def _print(self, *messages):
        if not self._verbose:
            sys.stdout.write("\033[F\033[K")
        print(''.join([str(m) for m in messages]))

    def _print_stats(self):
        self._print(f"[+] {self.__class__.__name__} ingested ",
                    f"{len(self.get('Resource'))} resources, ",
                    f"{len(self.get('Generic'))} generic resources were added\n")

    def load_generics(self, types=None):

        for k in self.types:

            self.add(Generic(properties={
                "Name": f"${k.split(':')[-1]}",
                "Arn":  RESOURCES.definition(k)
            }, labels=[k]))

    def load_resources(self):

        def get_resource_type_model(collection):

            service = self.__class__.__name__.capitalize()
            resource_model = collection.meta.resource_model._resource_defs
            remap = {k: k for k in resource_model.keys()}

            # Map model types to RESOURCE definitions
            for rt in resource_model.keys():

                for resource_type in sorted([k for k in resource_model.keys()
                                             if rt.startswith(k)], key=len, reverse=True):

                    remap[rt] = f"AWS::{service}::{resource_type}"

                    if remap[rt] in RESOURCES.types.keys():
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

                    # self._print(''.join((
                    #     f"[*] Skipped {label} ingestion ",
                    #     f"({', '.join(collateral)} will also be skipped)." if len(collateral) > 0 else "")))

                    continue

                rt = ''.join(''.join([f" {c}" if c.isupper() else c for c in getattr(
                    collections[0], attr)._model.request.operation]).split()[1:])

                for operation, collection in map(lambda c: (getattr(c, attr).all, c), collections):

                    for cm in operation():

                        collection_managers.append(cm)

                        if cm.meta.data is None:

                            # self._print(f"[*] Skipping ServiceResource {cm}: "
                            #                   "it has no properties")
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

                            # self._print(f"[-] Failed to construct resource ARN: defintion for type '{label}' is malformed - "
                            #                   f"boto collection '{cm.__class__.__name__}' does not have property {p}, "
                            #                   f"maybe you meant one of the following instead? {', '.join(properties.keys())}")
                            continue

                        # Add Resource
                        resource = Resource(labels=[label],
                                            properties=cm.meta.data)

                        if resource not in self:
                            self._print(f"[*] Adding {resource}")
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

        for resource in self.get("Resource"):

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
                    # self._print(f"Couldn't create association: resource ({arn}), "
                    #                    f"referenced by {resource}, doesn't exist ")
                    continue

                (source, target) = sorted((resource, associate),
                                          key=lambda r: r.id())

                self.add(Associative(properties={"Name": "Attached"},
                                     source=source, target=target))


class IAM(Ingestor):

    types = [
        "AWS::Iam::User", "AWS::Iam::Role", "AWS::Iam::Group",
        "AWS::Iam::Policy", "AWS::Iam::InstanceProfile",
        "AWS::Iam::MfaDevice", "AWS::Iam::VirtualMfaDevice"
    ]

    associations = [
        ("AWS::Iam::User", "AWS::Iam::VirtualMfaDevice")
    ]

    def __init__(self, session, resources=None, db="default.db", verbose=False, quick=False,
                 only_types=[], skip_types=[], only_arns=[], skip_arns=[]):

        self._db = db

        if resources is not None:
            self += resources
            return

        super().__init__(session=session, default=False, verbose=verbose, quick=False)

        self.client = self.session.client("iam")
        self.get_account_authorization_details(only_arns, skip_arns)

        if "AWS::Iam::User" in self.types:

            if "AWS::Iam::MfaDevice" in self.types or "AWS::Iam::VirtualMfaDevice" in self.types:
                self.list_users_mfa_devices()

            if not quick:
                self.get_login_profile()
                self.list_access_keys()

        # Set IAM entities
        self.entities = (
            self.get('AWS::Iam::User')
            + self.get('AWS::Iam::Role')
        ).get("Resource")

        # Set Account
        for a in set([e.account() for e in self.entities.get("Resource")]):
            self.account = a
            break

        self._print_stats()

    def get_account_authorization_details(self, only_arns, skip_arns):

        elements = Elements()
        edges = {
            "GroupNames": [],
            "Groups": [],
            "Policies": [],
            "InstanceProfiles": []
        }

        self._print("[*] Awaiting response to iam:GetAccountAuthorizationDetails "
                    "(this can take a while)")

        def get_aad_element(label, entry):

            properties = dict()
            for pk, pv in sorted(entry.items()):

                if pk.endswith("PolicyList"):
                    properties["Documents"] = [{
                        p["PolicyName"]: p["PolicyDocument"]
                        for p in pv}]

                elif pk == "AssumeRolePolicyDocument":
                    properties["Trusts"] = pv

                elif pk in ["GroupList", "InstanceProfileList", "AttachedManagedPolicies"]:
                    continue

                elif pk == "PolicyVersionList":

                    properties["Document"] = [{
                        "DefaultVersion": [p
                                           for p in pv
                                           if p["IsDefaultVersion"]
                                           ][0]["Document"]
                    }]

                else:
                    properties[pk.replace(label, "")] = pv

            element = Resource(
                properties=properties,
                labels=["Resource", f"AWS::Iam::{label}"])

            if f"AWS::Iam::Group" in self.types and "GroupList" in entry.keys():

                edges["GroupNames"].extend([(element, g)
                                            for g in entry["GroupList"]])

            if f"AWS::Iam::InstanceProfile" in self.types \
                    and "InstanceProfileList" in entry.keys():

                edges["InstanceProfiles"].extend([(get_aad_element("InstanceProfile", ip), element)
                                                  for ip in entry["InstanceProfileList"]])

            if f"AWS::Iam::Policy" in self.types \
                    and "AttachedManagedPolicies" in entry.keys():
                edges["Policies"].extend([(element, p["PolicyArn"])
                                          for p in entry["AttachedManagedPolicies"]])

            if (str(f"AWS::Iam::{label}") in self.types
                and (len(skip_arns) == 0 or properties["Arn"] not in skip_arns)
                and (len(only_arns) == 0 or properties["Arn"] in only_arns)
                    and element not in elements):
                self._print(f"[*] Adding {element}")
                elements.add(element)

            return element

        account_authorization_details = [aad for aad in self.client.get_paginator(
            "get_account_authorization_details"
        ).paginate()]

        account_authorization_details = [
            (label.replace("DetailList", "").replace("Policies", "Policy"), entry)
            for aad in account_authorization_details
            for (label, v) in aad.items() if isinstance(v, list)
            for entry in v]

        for label, entry in account_authorization_details:
            get_aad_element(label, entry)

        # Reconcile group names
        groups = elements.get("AWS::Iam::Group")
        for (element, groupname) in edges["GroupNames"]:
            group = next((g for g in groups if str(g).endswith(
                f":group/{groupname}")), None)
            if group is not None:
                edges["Groups"].append((element, group))

        # Ensure edge nodes exist
        for k, v in edges.items():
            edges[k] = list(filter(
                lambda e: e[0] is not None and e[1] is not None,
                [e if type(e[1]) == Resource
                 else (e[0], next((t for t in elements
                                   if str(t) == str(e[1])
                                   ), None))
                 for e in v]))

        # (:User|Group|Role)-[:TRANSITIVE{Attached}]->(:Policy)
        for (s, t) in edges["Policies"]:
            elements.add(Transitive(
                properties={"Name": "Attached"},
                source=s,
                target=t
            ))

        # (:User)-[:TRANSITIVE{MemberOf}]->(:Group)
        for (s, t) in edges["Groups"]:
            elements.add(Transitive(
                properties={"Name": "MemberOf"},
                source=s,
                target=t
            ))

        # (:InstanceProfile)-[:TRANSITIVE{Attached}]->(:Role)
        for (s, t) in edges["InstanceProfiles"]:
            del s.properties()["Roles"]
            elements.add(Transitive(
                properties={"Name": "Attached"},
                source=s,
                target=t))

        self.update(elements)

    def get_login_profile(self):

        for user in self.get("AWS::Iam::User").get("Resource"):

            try:
                login_profile = self.client.get_login_profile(
                    UserName=user.get("Name"))["LoginProfile"]
                del login_profile["UserName"]
                user.set("LoginProfile", login_profile)
                self._print("[+] Updated login profile "
                            f"information for {user}")

            except self.client.exceptions.NoSuchEntityException:
                pass

    def list_access_keys(self):

        for user in self.get("AWS::Iam::User").get("Resource"):

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
                self._print(f"[+] Updated access key information for {user}")

            except self.client.exceptions.NoSuchEntityException:
                pass

    def list_users_mfa_devices(self):

        self._print("[*] Listing user mfa devices")
        users = self.get("AWS::Iam::User").get("Resource")

        for user in users:

            for mfa_device in self.client.list_mfa_devices(
                UserName=user.properties()["Name"]
            )["MFADevices"]:

                label = RESOURCES.label(mfa_device["SerialNumber"])
                mfa_device["Arn"] = mfa_device["SerialNumber"]
                mfa_device["Name"] = mfa_device["Arn"].split('/')[-1] if label == "AWS::Iam::MfaDevice" \
                    else "Virtual Device" if label == "AWS::Iam::VirtualMfaDevice" \
                    else "Device"

                if label is None:
                    continue

                del mfa_device["SerialNumber"]
                del mfa_device["UserName"]

                resource = Resource(
                    labels=[label],
                    properties=mfa_device
                )

                associative = Associative(
                    properties={"Name": "Attached"},
                    source=user,
                    target=resource)

                self._print(f"[+] Adding {resource}")
                self.add(resource)
                self.add(associative)

    def post(self, skip_all_actions=False):
        if not skip_all_actions:
            self.add(Node(
                properties={
                    "Name": "CatchAll",
                    "Description": "Pseudo-Endpoint for actions that don't specify an affected resource type."
                },
                labels=["CatchAll"]))
            self.resolve()
        self.transitive()
        return self.save(self._db)

    def transitive(self):

        instances = self.get(
            "AWS::Ec2::Instance").get(
            "Resource")

        functions = self.get(
            "AWS::Lambda::Function").get(
            "Resource")

        roles = self.get(
            "AWS::Iam::Role").get(
            "Resource")

        instance_profiles = self.get(
            "AWS::Iam::InstanceProfile").get(
            "Resource")

        # Instance - [TRANSITIVE] -> Iam Instance Profile

        for instance in instances:

            if "IamInstanceProfile" not in instance.properties():
                continue

            target = next((ip for ip in instance_profiles
                           if ip.id() == instance.properties()["IamInstanceProfile"]["Arn"]),
                          None)

            del instance.properties()["IamInstanceProfile"]

            self.add(Transitive(
                {"Name": "Attached"}, source=instance, target=target))

        # Lambda - [TRANSITIVE] -> Role

        for function in functions:

            if "Role" not in function.properties():
                continue

            role = next((r for r in roles
                         if r.id() == function.properties()["Role"]),
                        None)

            del function.properties()["Role"]

            self.add(Transitive(
                {"Name": "Attached"}, source=function, target=role))

    def resolve(self):

        IDP = [
            "AWS::Iam::User",
            "AWS::Iam::Role",
            "AWS::Iam::Group",
            "AWS::Iam::Policy"
        ]

        RBP = {
            "AWS::S3::Bucket": "Policy",
            "AWS::S3::Object": "Policy",
            "AWS::Iam::Role": "Trusts"
        }

        (principals, actions, trusts) = (Elements(), Elements(), Elements())
        resources = self.get("Resource") + \
            self.get("Generic") + self.get("CatchAll")

        print("[*] Resolving actions and resources\n")

        # Resolve actions
        for resource in self.get("Resource"):

            self._print(f"[*] Processing {resource}")

            # Identity Based Policies (Inline and Managed)

            if resource.labels()[0] in IDP:

                count = len(actions)
                actions.update(IdentityBasedPolicy(
                    resource, resources).resolve())

                diff = len(actions) - count
                if diff > 0:
                    self._print(f"[+] Identity based Policy ({resource}) "
                                f"resolved to {diff} action(s)")

            if resource.labels()[0] in RBP.keys():

                # Bucket & Object ACLs

                if resource.type("AWS::S3::Bucket") or resource.type("AWS::S3::Object"):

                    count = len(actions)
                    if resource.type("AWS::S3::Bucket"):
                        acl = BucketACL(resource, resources)
                    elif resource.type("AWS::S3::Object"):
                        acl = ObjectACL(resource, resources)

                    principals.update(acl.principals())
                    actions.update(acl.resolve())

                    diff = len(actions) - count
                    if diff > 0:
                        self._print(f"[+] ACL for {resource} "
                                    f"resolved to {diff} action(s)")

                # Resource Based Policies

                rbp = ResourceBasedPolicy(
                    resource,
                    resources,
                    keys=[RBP[resource.labels()[0]]])

                if len(rbp.principals()) > 0:

                    count = len(actions)
                    resolved = rbp.resolve()

                    principals.update([p for p in rbp.principals()
                                       if p not in principals and
                                       str(p) != RESOURCES.types["AWS::Account"].format(Account=self.account)])

                    # TODO: This code should be moved to 'ResourceBasedPolicy' and override resolve().

                    # For Roles, actions imply a TRUSTS relationship. Only those beginning
                    # with sts:Assume are considered valid.

                    for action in [a for a in resolved
                                   if "AWS::Iam::Role" not in resource.labels() or
                                   str(a).startswith("sts:AssumeRole")]:

                        if action.source().type("AWS::Account") \
                                and action.source().properties()["Arn"].split(':')[4] == self.account:

                            if "AWS::Iam::Role" in resource.labels():

                                trusts.update([Trusts(properties=action.properties(),
                                                      source=action.target(),
                                                      target=e)
                                               for e in self.entities])

                            # This case appears redundant for Buckets

                        else:
                            if not action.source().type("AWS::Domain"):
                                actions.add(action)

                            if "AWS::Iam::Role" in resource.labels():
                                trusts.add(Trusts(properties=action.properties(),
                                                  source=action.target(),
                                                  target=action.source()))

                    diff = len(actions) - count
                    if diff > 0:
                        self._print(f"[+] Resource based policy ({resource}) "
                                    f"resolved to {diff} action(s)")

        self.update(principals)
        self.update(actions)
        self.update(trusts)

        sys.stdout.write("\033[F\033[K")
        print(f"[+] Produced {len(principals)} "
              f"new principals and {len(actions)} actions\n")


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

    def __init__(self, session, account="000000000000", verbose=False, quick=False,
                 only_types=[], skip_types=[], only_arns=[], skip_arns=[]):

        super().__init__(session=session, account=account, verbose=verbose, quick=quick,
                         only_types=only_types, skip_types=skip_types,
                         only_arns=only_arns, skip_arns=skip_arns)

        self.client = self.session.client("ec2")

        if not quick:
            self.get_instance_user_data()

        super()._print_stats()

    def get_instance_user_data(self):

        for instance in self.get("AWS::Ec2::Instance").get("Resource"):

            name = instance.get("Name")

            try:
                response = self.client.describe_instance_attribute(Attribute="userData",
                                                                   DryRun=False,
                                                                   InstanceId=name)
            except ClientError as e:
                self._print("[!] Couldn't get user data for "
                            f"{name} -- it may no longer exist.")

            if 'UserData' in response.keys() and 'Value' in response['UserData'].keys():
                userdata = b64decode(response['UserData']['Value'])
                if userdata[0: 2] == b'\x1f\x8b':  # it's gzip data
                    userdata = zlib.decompress(
                        userdata, zlib.MAX_WBITS | 32).decode('utf-8')
                else:  # normal b64
                    userdata = userdata.decode('utf-8')

                instance.set("UserData", {"UserData": userdata})
                self._print(f"[+] Updated instance user data for {instance}")


class S3(Ingestor):

    types = [
        'AWS::S3::Bucket',
        'AWS::S3::Object',
    ]

    associations = [
        ('AWS::S3::Bucket', 'AWS::S3::Object')
    ]
    def __init__(self, session, account="000000000000", verbose=False, quick=False,
                 only_types=[], skip_types=[], only_arns=[], skip_arns=[]):

        super().__init__(session=session, account=account, verbose=verbose, quick=quick,
                         only_types=only_types, skip_types=skip_types,
                         only_arns=only_arns, skip_arns=skip_arns)

        self.client = self.session.client('s3')

        if not quick:
            self.get_bucket_policies()
            self.get_bucket_acls()
            self.get_public_access_blocks()
            self.get_object_acls()

        self._print_stats()

    def get_bucket_policies(self):

        for bucket in self.get("AWS::S3::Bucket").get("Resource"):

            try:
                policy = self.client.get_bucket_policy(
                    Bucket=bucket.get('Name'))["Policy"]

                bucket.set("Policy", json.loads(policy))
                self._print(f"[+] Updated Bucket ({bucket}) policy")

            except ClientError as e:
                self._print("[-] Failed to update Bucket policy "
                            f"({bucket}): {str(e)}")

    def get_public_access_blocks(self):

        for bucket in self.get("AWS::S3::Bucket").get("Resource"):

            # https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html
            # Implicitly affects Bucket ACLs and Policies (values returned by associated get requests
            # specify what is being enforced rather than actual values)

            try:
                public_access_block = self.client.get_public_access_block(
                    Bucket=bucket.get("Name")
                )["PublicAccessBlockConfiguration"]

                bucket.set("PublicAccessBlock", public_access_block)
                self._print(
                    f"[+] Updated Bucket ({bucket}) public access block")

            except ClientError as e:
                self._print("[-] Failed to update Bucket public access block "
                            f"({bucket}): {str(e)}")

    def get_bucket_acls(self):

        for bucket in self.get("AWS::S3::Bucket").get("Resource"):

            try:
                acl = self.client.get_bucket_acl(Bucket=bucket.get('Name'))
                bucket.set("ACL", {
                    "Owner": acl["Owner"],
                    "Grants": acl["Grants"]
                })
                self._print(f"[+] Updated Bucket ({bucket}) ACL")

            except ClientError as e:
                self._print("[-] Failed to update Bucket ACL "
                            f"({bucket}): {str(e)}")

    def get_object_acls(self):

        for obj in self.get("AWS::S3::Object").get("Resource"):

            try:
                arn = obj.get("Arn")
                bucket, *key = arn.split(':::')[1].split('/')
                key = "/".join(key)

                acl = self.client.get_object_acl(Bucket=bucket, Key=key)
                obj.set("ACL", {
                    "Owner": acl["Owner"],
                    "Grants": acl["Grants"]
                })
                self._print(f"[+] Updated Object ({obj}) ACL")

            except ClientError as e:
                self._print("[-] Failed to update Object ACL "
                            f"({obj}): {str(e)}")


class Lambda(Ingestor):

    types = [
        'AWS::Lambda::Function',
    ]

    def __init__(self, session, account="000000000000", verbose=False, quick=False,
                 only_types=[], skip_types=[], only_arns=[], skip_arns=[]):

        super().__init__(session=session, default=False, verbose=verbose, quick=quick)

        self.client = self.session.client('lambda')
        self.list_functions()

        super()._print_stats()

    def list_functions(self):

        functions = Elements()
        self._print("[*] Listing functions (this can take a while)")
        for function in [f
                         for r in self.client.get_paginator("list_functions").paginate()
                         for f in r["Functions"]]:

            function["Name"] = function["FunctionName"]
            function["Arn"] = function["FunctionArn"]
            del function["FunctionName"]
            del function["FunctionArn"]

            f = Resource(
                properties=function,
                labels=["AWS::Lambda::Function"])

            if f not in functions:
                self._print(f"[*] Adding {f}")
                functions.add(f)

        self.update(functions)
