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

    run = []
    associates = []

    def __init__(self, session, account="000000000000", default=True, verbose=True, quick=False,
                 only_types=[], skip_types=[], only_arns=[], skip_arns=[]):

        self.session = session
        self.account_id = account
        self.run_all = len(self.run) == 0
        self._verbose = verbose
        self._load_generics()

        if default and len(self.run) > 0:

            self.run = [t for t in self.run
                        if (len(skip_types) == 0 or t not in skip_types)
                        and (len(only_types) == 0 or t in only_types)]

            self.only_arns = only_arns
            self.skip_arns = skip_arns

            print("[*] Commencing {resources} ingestion\n".format(
                ingestor=self.__class__.__name__,
                resources=', '.join([
                    r if (i == 0 or i % 3 > 0)
                    else f'\n{" " * 15}{r}'
                    for i, r in enumerate(self.run)])
            ))

            self._load_resources()
            self._load_associations()

    def _print(self, *messages):
        if not self._verbose:
            sys.stdout.write("\033[F\033[K")
        print(''.join([str(m) for m in messages]))

    def _print_stats(self):
        self._print(f"[+] {self.__class__.__name__} ingested ",
                    f"{len(self.get('Resource'))} resources, ",
                    f"{len(self.get('Generic'))} generic resources were added\n")

    def _resolve_arn_selection(self, only_arns=[], skip_arns=[]):
        """
        Set only/except ARNS for this ingestor.
        """

        if only_arns and skip_arns:
            print("[!] Can't specify both --only-arns and --skip-arns.")
            return False

        self.only_arns = self._filter_arns(only_arns)
        self.skip_arns = self._filter_arns(skip_arns)

        return True

    def _filter_arns(self, arns):
        """ From a list of ARNs, return only those relevant to this ingestor's service. """
        return [a for a in arns if self.__class__.__name__.lower() == a.split(":")[2].lower()]

    def _load_resources(self, boto_base_resource=None, awspx_base_resource=None):

        if boto_base_resource is None:
            boto_base_resource = self.session.resource(
                self.__class__.__name__.lower())

        for rt in self._get_collections(boto_base_resource):
            self._load_resource_collection(
                rt,
                boto_base_resource,
                awspx_base_resource
            )

    # Needs to be recursive
    def _load_resource_collection(self,
                                  collection,
                                  boto_base_resource=None,
                                  awspx_base_resource=None):

        resources = []

        label = "AWS::{service}::{type}".format(
            service=self.__class__.__name__.capitalize(),
            type=getattr(
                boto_base_resource,
                collection
            )._model.resource.type
        )

        # Known cases of misaligned naming conventions (boto and lib.aws.RESOURCES)
        if label.endswith("Version"):
            label = label[:-7]
        elif label == "AWS::Ec2::KeyPairInfo":
            label = "AWS::Ec2::KeyPair"

        # Skip excluded types or types unknown to us
        if label not in RESOURCES.types \
                or (not self.run_all and label not in self.run):
            return

        try:
            # Note: Depending on the stage at which the exception is thrown, we
            # may miss certain resources.

            resources = [r for r in getattr(
                boto_base_resource,
                collection).all()]

        except Exception as e:
            self._print(f"[!] Couldn't load {collection} of {boto_base_resource} "
                        "-- probably due to a resource based policy or something.")

        for resource in resources:

            # Get properties
            properties = resource.meta.data

            if properties is None:
                continue

            # Get Arn and Name
            arn = self._get_resource_arn(resource, boto_base_resource)
            name = self._get_resource_name(resource)

            # Include or exclude this ARN
            if self.only_arns and arn not in self.only_arns:
                continue
            elif self.skip_arns and arn in self.skip_arns:
                continue

            properties["Arn"] = arn
            properties["Name"] = name

            if not (properties["Arn"] and properties["Name"]):
                print(label)
                print(json.dumps(properties, indent=2, default=str))
                raise ValueError

            # Create resource
            r = Resource(labels=[label], properties=properties)
            if r not in self:
                self._print(f"[*] Adding {r}")
                self.add(r)

            # Add associative relationship with parent
            if awspx_base_resource:
                assocs = [set(a) for a in self.associates]
                if {awspx_base_resource.labels()[0], r.labels()[0]} in assocs \
                        or not self.associates:
                    e = Associative(properties={"Name": "Attached"},
                                    source=r, target=awspx_base_resource)
                    oe = Associative(properties={"Name": "Attached"},
                                     source=awspx_base_resource, target=r)
                    if not (e in self or oe in self):
                        self.add(e)

            # Load resources from this one's collections
            if self._get_collections(resource):
                self._load_resources(resource, r)

            # Return when we've seen all explicit resources
            if self.only_arns and all([
                    r in map(lambda x: x.id(), self)
                    for r in self.only_arns]):
                return

    def _get_resource_arn(self, resource, base_resource):

        resource_type = resource.__class__.__name__.split(".")[-1]
        properties = resource.meta.data
        keys = properties.keys()
        label = self._get_resource_type_label(resource_type)
        arn = None

        if "Arn" in keys:
            arn = properties["Arn"]
        elif f"{resource_type}Arn" in keys:
            arn = properties[f"{resource_type}Arn"]
        elif f"{resource_type}Id" in keys and properties[f"{resource_type}Id"].startswith("arn:aws"):
            arn = properties[f"{resource_type}Id"]
        elif label in RESOURCES.keys():
            parent = base_resource.meta.data if base_resource.meta.data is not None else {}
            combined = {**parent, **properties}
            arn = RESOURCES.definition(label).format(
                Region=self.session.region_name,
                Account=self.account_id,
                **combined)

        if isinstance(arn, str) \
                and re.compile("arn:aws:([a-zA-Z0-9]+):([a-z0-9-]*):(\d{12}|aws)?:(.*)"
                               ).match(arn) is not None:
            return arn

        return None

    def _get_resource_name(self, resource):

        resource_type = resource.__class__.__name__.split(".")[-1]
        properties = resource.meta.data
        keys = properties.keys()

        if "Name" in keys:
            return properties["Name"]
        elif f"{resource_type}Name" in keys:
            return properties[f"{resource_type}Name"]
        elif "Id" in keys and not properties["Id"].startswith("arn:aws"):
            return properties["Id"]
        elif f"{resource_type}Id" in keys and not properties[f"{resource_type}Id"].startswith("arn:aws"):
            return properties[f"{resource_type}Id"]
        elif "Key" in keys:
            return properties["Key"]
        else:
            # Irregular variants: e.g. KeyName for KeyPairs
            key = [k for k in
                   [k for k in keys if "Name" in k]
                   if k.replace("Name", "") in resource_type
                   ][0]
            return properties[key]

    def _get_resource_type_label(self, resource_type):

        return "AWS::%s::%s" % (
            self.__class__.__name__.capitalize(),
            resource_type.replace("Info", "").replace("Version", "").replace("Summary", ""))

    def _load_generics(self, types=None):

        labels = [t for t in types if t in RESOURCES]  \
            if types is not None else \
            [t for t in RESOURCES if t.startswith(
                "AWS::%s::" % self.__class__.__name__.capitalize())]

        for k in labels:

            self.add(Generic(properties={
                "Name": "$%s" % k.split(':')[-1],
                "Arn":  RESOURCES.definition(k)
            }, labels=[k]))

    def _load_associations(self):

        if len(self.associates) == 0:
            return

        edges = Elements()
        self._print(f"[*] Adding {self.__class__.__name__} "
                    "associative relationships")

        for resource in self.get("Resource"):

            references = {}
            label = [l for l in resource.labels() if l != "Resource"][0]

            # Find references to other resources in the form of a dictionary (refs)

            self._references(resource.properties(), references)

            # Create an edge, for all known associations (as defined by self.rels).

            for rel in [r for r in self.associates if r[0] == label or r[1] == label]:

                i = 1 if label == rel[0] else 0

                # Get a list of foreign keys that we must be capable of referencing
                # in order to create an association

                fk = [a for a in re.compile(
                    "{([A-Za-z]+)}").findall(RESOURCES.definition(rel[i]))
                    if a not in ["Account", "Region"]]

                if not all([k in references.keys() for k in fk]):
                    continue

                # TODO: Handle Types that make use of more than one
                # variable identifier

                if len(fk) != 1:
                    raise NotImplementedError

                fk = fk[0]

                for v in list(references[fk]):

                    # Find the first resource matching the reference

                    r = next((r for r in self if re.compile(
                        RESOURCES.definition(rel[i]).format(
                            Account=self.account_id,
                            Region=self.session.region_name,
                            **{
                                **{x: list(y)[0] for x, y in references.items() if len(y) == 1},
                                **{fk: v}
                            })
                    ).match(str(r.id())) is not None), None)

                    if r is None:
                        # print("Failed to match (%s: %s) against any resources" % (k, v))
                        # print("Its likely that the resource was missed during ingestion")
                        continue

                    # Delete the properties that are responsible for the edge's existence.

                    properties = self._extract_property_value(
                        resource.properties(), fk)

                    # Even though direction is irrelavent when dealing with Associative
                    # edges, neo4j is directed. We need to ensure the direction is kept
                    # in order to eliminate duplicate edges.

                    (source, target) = (resource, r) if i == 1 else (r, resource)

                    edge = Associative(
                        properties={"Name": "Attached"}, source=source, target=target)
                    opposite_edge = Associative(
                        properties={"Name": "Attached"}, source=target, target=source)

                    if (edge not in self and opposite_edge not in self) and edge not in edges:
                        edges.add(edge)

        self.update(edges)

    def _extract_property_value(self, properties, key, depth=None):

        def get_dereference_indexes(properties, value, keys=[]):

            if isinstance(properties, dict):

                for k, v in properties.items():
                    if k == value:
                        return keys + [value]

                    r = get_dereference_indexes(
                        v, value, keys + [k])
                    if r is not None:
                        return r

                return None

            elif isinstance(properties, list):

                for i in range(len(properties)):

                    r = get_dereference_indexes(
                        properties[i], value, keys + [i])
                    if r is not None:
                        return r

            return None

        dereferences = get_dereference_indexes(properties, key)

        # Key not present in properties

        if dereferences is None or len(dereferences) == 0:
            return {}

        # Set the depth to max

        if depth is None:
            depth = len(dereferences) - 1

        depth *= -1

        backup = copy.deepcopy(reduce(lambda x, y: x[y],
                                      dereferences[:depth] if depth != 0 else dereferences,
                                      properties))

        reduce(lambda x, y: x[y], dereferences[:depth-1],
               properties).pop(dereferences[depth-1])

        return backup

    def _get_collections(self, resource):

        return [attribute for attribute in dir(resource)
                if boto3.resources.collection.CollectionManager
                in getattr(resource, attribute).__class__.__bases__]

    def _references(self, value, references={}, key=None):

        if isinstance(value, list):
            [self._references(v, references)
             for v in value]

        elif isinstance(value, dict):
            [self._references(v, references, k)
             for k, v in value.items()]

        elif key is not None \
                and key != "Arn" \
                and key != "Name" \
                and isinstance(value, str) \
                and len(value) > 0 \
                and (key.endswith("Id") or key.endswith("Arn") or key.endswith("Name")):

            if key not in references:
                references[key] = set()

            references[key].update([value])


class IAM(Ingestor):

    run = ["AWS::Iam::User", "AWS::Iam::Role", "AWS::Iam::Group",
           "AWS::Iam::Policy", "AWS::Iam::InstanceProfile"]

    def __init__(self, session, resources=None, db="default.db", verbose=False, quick=False,
                 only_types=[], skip_types=[], only_arns=[], skip_arns=[]):

        self._db = db
        self._verbose = verbose
        self.account_id = "000000000000"

        if resources is not None:
            self += resources
            return

        super().__init__(session=session, default=False, verbose=verbose, quick=False)

        self.client = self.session.client("iam")

        self.run = [r for r in self.run
                    if (len(only_types) == 0 or r in only_types)
                    and r not in skip_types]

        print("[*] Commencing {resources} ingestion\n".format(
            resources=', '.join([r if (i == 0 or i % 3 > 0) else f'\n{" " * 15}{r}'
                                 for i, r in enumerate(self.run)])))

        self.get_account_authorization_details(only_arns, skip_arns)

        if not quick:

            if "AWS::Iam::User" in self.run:
                self.get_login_profile()
                self.list_access_keys()

        # Set IAM entities
        self.entities = (
            self.get('AWS::Iam::User')
            + self.get('AWS::Iam::Role')
        ).get("Resource")

        # Set Account
        for a in set([e.account() for e in self.entities.get("Resource")]):
            self.account_id = a
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

            if f"AWS::Iam::Group" in self.run and "GroupList" in entry.keys():

                edges["GroupNames"].extend([(element, g)
                                            for g in entry["GroupList"]])

            if f"AWS::Iam::InstanceProfile" in self.run \
                    and "InstanceProfileList" in entry.keys():

                edges["InstanceProfiles"].extend([(get_aad_element("InstanceProfile", ip), element)
                                                  for ip in entry["InstanceProfileList"]])

            if f"AWS::Iam::Policy" in self.run \
                    and "AttachedManagedPolicies" in entry.keys():
                edges["Policies"].extend([(element, p["PolicyArn"])
                                          for p in entry["AttachedManagedPolicies"]])

            if (str(f"AWS::Iam::{label}") in self.run
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
                                       str(p) != RESOURCES.types["AWS::Account"].format(Account=self.account_id)])

                    # TODO: This code should be moved to 'ResourceBasedPolicy' and override resolve().

                    # For Roles, actions imply a TRUSTS relationship. Only those beginning
                    # with sts:Assume are considered valid.

                    for action in [a for a in resolved
                                   if "AWS::Iam::Role" not in resource.labels() or
                                   str(a).startswith("sts:AssumeRole")]:

                        if action.source().type("AWS::Account") \
                                and action.source().properties()["Arn"].split(':')[4] == self.account_id:

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

    run = [
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

    associates = [
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

        if not quick:
            self.get_instance_user_data()

        super()._print_stats()

    def get_instance_user_data(self):

        client = self.session.client(self.__class__.__name__.lower())

        for instance in self.get("AWS::Ec2::Instance").get("Resource"):

            name = instance.get("Name")

            try:
                client.describe_instance_attribute(
                    Attribute="userData", DryRun=True, InstanceId=name)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    self._print(
                        "[!] EC2: Not authorised to get instance user data.")

            try:
                response = client.describe_instance_attribute(Attribute="userData",
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

    run = [
        'AWS::S3::Bucket',
        'AWS::S3::Object',
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

        sr = self.session.resource(self.__class__.__name__.lower())

        for bucket in self.get("AWS::S3::Bucket").get("Resource"):
            try:
                bucket.set("Policy", json.loads(sr.BucketPolicy(
                    bucket.get('Name')).policy))
                self._print(f"[+] Updated bucket policy for {bucket}")
            # No policy for this bucket
            except:
                pass

    def get_bucket_acls(self):

        sr = self.session.resource(self.__class__.__name__.lower())

        for bucket in self.get("AWS::S3::Bucket").get("Resource"):
            try:
                bucket.set("ACL", sr.BucketAcl(bucket.get('Name')).grants)
                self._print(f"[+] Updated bucket acl for {bucket}")
            except ClientError as e:
                if "AccessDenied" in str(e):
                    self._print(
                        f"[!] Access denied when getting ACL for {bucket}")
                else:
                    self._print("[!]", e)

    def get_object_acls(self):

        sr = self.session.resource(self.__class__.__name__.lower())

        for obj in self.get("AWS::S3::Object").get("Resource"):
            try:
                arn = obj.get("Arn")
                bucket, *key = arn.split(':::')[1].split('/')
                key = "/".join(key)
                obj.set("ACL", sr.ObjectAcl(bucket, key).grants)
                self._print(f"[+] Updated object acl for {obj}")
            except ClientError as e:
                if "AccessDenied" in str(e):
                    self._print(
                        f"[!] Access denied when getting ACL for {obj}")
                else:
                    self._print("[!]", e)

    def get_public_access_blocks(self):

        for bucket in self.get("AWS::S3::Bucket").get("Resource"):

            try:
                # https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html
                # Implicitly affects Bucket ACLs and Policies (values returned by associated get requests
                # specify what is being enforced rather than actual values)

                bucket.set("PublicAccessBlock",
                           self.client.get_public_access_block(
                               Bucket=bucket.get("Name")
                           )["PublicAccessBlockConfiguration"])

            except Exception:
                pass


class Lambda(Ingestor):
    run = [
        'AWS::Lambda::Function',
    ]

    def __init__(self, session, account="000000000000", verbose=False, quick=False,
                 only_types=[], skip_types=[], only_arns=[], skip_arns=[]):

        super().__init__(session=session, default=False, verbose=verbose, quick=quick)

        self.run = [t for t in self.run
                    if (len(skip_types) == 0 or t not in skip_types)
                    and (len(only_types) == 0 or t in only_types)]

        if len(self.run) == 0:
            return

        self.client = self.session.client('lambda')

        print("[*] Commencing {resources} ingestion".format(
            ingestor=self.__class__.__name__,
            resources=', '.join([
                r if (i == 0 or i % 3 > 0)
                else f'\n{" " * 15}{r}'
                for i, r in enumerate(self.run)])
        ))

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
