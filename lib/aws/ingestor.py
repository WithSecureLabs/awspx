import copy
import re
import json
import zlib
import inflect
from base64 import b64decode
from functools import reduce

import boto3
from botocore.exceptions import ClientError

from lib.aws.actions import ACTIONS
from lib.aws.resources import RESOURCES

from lib.graph.base import Elements
from lib.graph.edges import Action, Associative, Transitive, Trusts
from lib.graph.nodes import Generic, Resource
from lib.graph.db import Neo4j

from lib.aws.policy import BucketACL, IdentityBasedPolicy, ResourceBasedPolicy


class Ingestor(Elements):

    run = []
    associates = []

    def __init__(self, session, account="0000000000000", default=True, only_types=[], except_types=[], only_arns=[], except_arns=[]):

        self.session = session
        self.account_id = account

        if not (self._resolve_type_selection(only_types, except_types)
                and self._resolve_arn_selection(only_arns, except_arns)):
            return

        if default:

            resources = [
                f"AWS::{self.__class__.__name__}::" + ''.join(list(map(
                    lambda x: x[0].capitalize() + x[1:],
                    str(x).split('_'))))[:-1] + "s" for x in self.run
            ]

            print("Ingesting {resources} from {ingestor}".format(
                ingestor=self.__class__.__name__,
                resources=', '.join(resources)
            ))

            self._load_resources()
            self._load_associations()

        self._load_generics()

    def _resolve_type_selection(self, only_types=[], except_types=[]):
        """
        Change run list to reflect only/except selection made by user.
        """

        if only_types and except_types:
            print("Can't specify both --only-resource-types and --except-resource-types.")
            return False

        if only_types:
            only_types = self._type_to_run(only_types)
            self.run = list(set(self.run) & set(only_types))
        elif except_types:
            except_types = self._type_to_run(except_types)
            self.run = list(set(self.run) - set(except_types))

        return True

    def _type_to_run(self, types):
        """
        Convert list of formal types to run list, filtering out types for other ingestors.

        e.g. S3 ingestor ["AWS::EC2:Instance","AWS::S3::Bucket"]
             -> ["buckets"]
        """

        inf = inflect.engine()
        return [inf.plural(i.split('::')[-1]).lower() for i in types
                if i.split('::')[1].lower() == self.__class__.__name__.lower()]

    def _resolve_arn_selection(self, only_arns=[], except_arns=[]):
        """
        Set only/except ARNS for this ingestor.
        """

        if only_arns and except_arns:
            print("Can't specify both --only-resource-arns and --except-resource-arns.")
            return False

        self.only_arns = self._filter_arns(only_arns)
        self.except_arns = self._filter_arns(except_arns)

        return True

    def _filter_arns(self, arns):
        """ From a list of ARNs, return only those relevant to this ingestor's service. """
        return [a for a in arns if self.__class__.__name__.lower() == a.split(":")[2].lower()]

    def _load_resources(self, boto_base_resource=None, awspx_base_resource=None):

        if boto_base_resource is None:
            boto_base_resource = self.session.resource(
                self.__class__.__name__.lower())

        for rt in self._get_collections(boto_base_resource):
            if rt in self.run or not self.run:  # ingest everything if list is empty
                self._load_resource_collection(
                    rt, boto_base_resource, awspx_base_resource)

    def _load_resource_collection(self,
                                  collection,
                                  boto_base_resource=None,
                                  awspx_base_resource=None):

        resources = []

        try:

            # Note: Depending on the stage at which the exception is thrown, we
            # may miss certain resources.

            resources = [r for r in getattr(
                boto_base_resource, collection).all()]

        except Exception as e:
            print(f"Couldn't load {collection} of {boto_base_resource} "
                  "- probably due to a resource based policy or something.")

        for resource in resources:

            # Get properties
            properties = resource.meta.data
            if properties is None:
                continue

            # Get label
            resource_type = resource.__class__.__name__.split(".")[-1]
            label = self._get_resource_type_label(resource_type)

            # Get Arn and Name
            arn = self._get_resource_arn(resource, boto_base_resource)
            name = self._get_resource_name(resource)

            # Include or exclude this ARN
            if self.only_arns and arn not in self.only_arns:
                continue
            elif self.except_arns and arn in self.except_arns:
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
                print(f" \-> Adding {r}")
                self.append(r)

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
                        self.append(e)

            # Load resources from this one's collections
            if self._get_collections(resource):
                self._load_resources(resource, r)

            # Return when we've seen all explicit resources
            if self.only_arns and all([r in map(lambda x: x.id(), self) for r in self.only_arns]):
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

        if isinstance(arn, str) and re.compile(
                "arn:aws:([a-zA-Z0-9]+):([a-z0-9-]*):(\d{12})?:(.*)").match(arn) is not None:
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

            self.append(Generic(properties={
                "Name": "$%s" % k.split(':')[-1],
                "Arn":  RESOURCES.definition(k)
            }, labels=[k]))

    def _load_associations(self):

        if len(self.associates) == 0:
            return

        edges = Elements()

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
                    ).match(r.id()) is not None), None)

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
                        edges.append(edge)

        self.extend(edges)

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

    def __init__(self, session, resources=None, db="default.db"):

        super().__init__(session=session, default=False)

        self._db = db

        if resources is None:

            self.client = self.session.client("iam")

            print("[+] Ingesting AWS::Iam::Users, AWS::Iam::Roles, ",
                  "AWS::Iam::Groups, AWS::Iam::Policies, "
                  "AWS::Iam::InstanceProfiles from IAM")

            self += self.get_account_authorization_details()
            self.get_login_profile()
            self.list_access_keys()

        elif len(resources) > 0:
            self += resources

        # Set IAM entities
        self.entities = Elements(
            self.get('AWS::Iam::User') + self.get('AWS::Iam::Role')
        ).get("Resource")

        # Set Account
        for a in set([e.account() for e in self.entities.get("Resource")]):
            self.root = Resource(
                properties={"Name": a, "Arn": "arn:aws:iam::%s:root" % a},
                labels=["Resource", "AWS::Iam::Root"])
            break

    def get_account_authorization_details(self):

        elements = Elements()
        edges = {
            "Groups": [],
            "Policies": [],
            "InstanceProfiles": []
        }

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
                labels=["Resource", "AWS::Iam::%s" % label])

            if "GroupList" in entry.keys():

                edges["Groups"].extend(
                    [(element, g) for g in entry["GroupList"]])

            if "InstanceProfileList" in entry.keys():

                edges["InstanceProfiles"].extend([
                    (get_aad_element("InstanceProfile", ip), element)
                    for ip in entry["InstanceProfileList"]])

            if "AttachedManagedPolicies" in entry.keys():
                edges["Policies"].extend([
                    (element, p["PolicyArn"])
                    for p in entry["AttachedManagedPolicies"]])

            if element not in elements:
                print(f" \-> Adding {element}")
                elements.append(element)

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

        # User|Group|Role - Attached -> Policy

        for (s, t) in edges["Policies"]:
            t = next(entry for entry in elements if entry.id() == t)
            elements.append(Transitive(
                properties={"Name": "Attached"}, source=s, target=t))

        # User - [MemberOf] -> Group

        for (s, t) in edges["Groups"]:
            t = next(entry for entry in elements.get(
                "AWS::Iam::Group") if str(entry).endswith(t))
            elements.append(Transitive(
                properties={"Name": "MemberOf"}, source=s, target=t))

        # InstanceProfile - [Attached] -> Role

        for (s, t) in edges["InstanceProfiles"]:
            del s.properties()["Roles"]
            elements.append(Transitive(
                properties={"Name": "Attached"}, source=s, target=t))

        return elements

    def get_login_profile(self):

        for user in self.get("AWS::Iam::User").get("Resource"):

            try:
                login_profile = self.client.get_login_profile(
                    UserName=user.get("Name"))["LoginProfile"]
                del login_profile["UserName"]
                user.set("LoginProfile", login_profile)

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

            except self.client.exceptions.NoSuchEntityException:
                pass

    def post(self):
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

            self.append(Transitive(
                {"Name": "Attached"}, source=instance, target=target))

        # Lambda - [TRANSITIVE] -> Role

        for function in functions:

            if "Role" not in function.properties():
                continue

            role = next((r for r in roles
                         if r.id() == function.properties()["Role"]),
                        None)

            del function.properties()["Role"]

            self.append(Transitive(
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
            "AWS::Iam::Role": "Trusts"
        }

        (principals, actions, trusts) = (Elements(), Elements(), Elements())
        resources = self.get("Resource") + self.get("Generic")

        print("Resolving actions and resources")

        # Resolve actions
        for resource in self.get("Resource"):

            # Identity Based Policies (Inline and Managed)

            if resource.labels()[0] in IDP:

                count = len(actions)
                actions.extend(IdentityBasedPolicy(
                    resource, resources).resolve())

                diff = len(actions) - count
                if diff > 0:
                    print(f"[+] Identity based Policy for `{resource}` "
                          f"resolved to {diff} action(s)")

            if resource.labels()[0] in RBP.keys():

                # Bucket ACLs

                if resource.type("AWS::S3::Bucket"):

                    count = len(actions)
                    acl = BucketACL(resource, resources)

                    principals.extend(
                        [p for p in acl.principals() if p not in principals])
                    actions.extend(
                        [a for a in acl.resolve() if a not in actions])

                    diff = len(actions) - count
                    if diff > 0:
                        print(f"[+] Bucket ACL for `{resource}` "
                              f"resolved to {diff} action(s)")

                # Resource Based Policies

                rbp = ResourceBasedPolicy(
                    resource,
                    resources,
                    keys=[RBP[resource.labels()[0]]])

                if len(rbp.principals()) > 0:

                    count = len(actions)
                    resolved = rbp.resolve()

                    principals.extend([p for p in rbp.principals()
                                       if p not in principals and
                                       str(p) != RESOURCES.types["AWS::Account"].format(Account=self.root.account())])

                    # TODO: This code should be moved to 'ResourceBasedPolicy' and override resolve().

                    # For Roles, actions imply a TRUSTS relationship. For both (ACTION and TRUSTS, only actions beginning
                    # with sts:Assume are considered valid.

                    for action in [a for a in resolved
                                   if "AWS::Iam::Role" not in resource.labels() or
                                   str(a).startswith("sts:AssumeRole")]:

                        if action.source().type("AWS::Account") \
                                and action.source().properties()["Arn"].split(':')[4] == self.root.account():

                            if "AWS::Iam::Role" in resource.labels():

                                trusts.extend([Trusts(properties=action.properties(),
                                                      source=action.target(),
                                                      target=e)
                                               for e in self.entities])

                            # This case appears redundant for Buckets

                        else:
                            actions.append(action)
                            if "AWS::Iam::Role" in resource.labels():
                                trusts.append(Trusts(properties=action.properties(),
                                                     source=action.target(),
                                                     target=action.source()))

                    diff = len(actions) - count

                    if diff > 0:
                        print(f"[+] Resource based policy for `{resource}` "
                              f"resolved to {diff} action(s)")

        self.extend([p for p in principals if p not in self])
        self.extend([a for a in actions if a not in self])
        self.extend(trusts)


class EC2(Ingestor):

    run = [
        'classic_addresses',  # What is this?
        'dhcp_options_sets',
        # 'images',
        'instances',
        'internet_gateways',
        'key_pairs',
        'network_acls',
        'network_interfaces',
        'placement_groups',
        'route_tables',
        'security_groups',
        # 'snapshots',
        'subnets',
        'volumes',
        # 'vpc_addresses',
        'vpc_peering_connections',
        'vpcs',
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

    def __init__(self, session, account="0000000000000", only_types=[], except_types=[], only_arns=[], except_arns=[]):

        super().__init__(session=session, account=account, default=True, only_types=only_types,
                         except_types=except_types, only_arns=only_arns, except_arns=except_arns)

        self.get_instance_user_data()

    def get_instance_user_data(self):

        client = self.session.client(self.__class__.__name__.lower())

        for instance in self.get("AWS::Ec2::Instance").get("Resource"):

            name = instance.get("Name")

            try:
                client.describe_instance_attribute(
                    Attribute="userData", DryRun=True, InstanceId=name)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    print("EC2: Not authorised to get instance user data.")

            response = client.describe_instance_attribute(Attribute="userData",
                                                          DryRun=False,
                                                          InstanceId=name)
            if 'UserData' in response.keys() and 'Value' in response['UserData'].keys():
                userdata = b64decode(response['UserData']['Value'])
                if userdata[0:2] == b'\x1f\x8b':  # it's gzip data
                    userdata = zlib.decompress(
                        userdata, zlib.MAX_WBITS | 32).decode('utf-8')
                else:  # normal b64
                    userdata = userdata.decode('utf-8')

                instance.set("UserData", {"UserData": userdata})


class S3(Ingestor):

    run = [
        'buckets',
        'objects',
        # 'object_versions',
        # 'multipart_uploads'
    ]

    def __init__(self, session, account="0000000000000", only_types=[], except_types=[], only_arns=[], except_arns=[]):

        super().__init__(session=session, account=account, default=True, only_types=only_types,
                         except_types=except_types, only_arns=only_arns, except_arns=except_arns)

        self.get_bucket_policies()
        self.get_bucket_acls()

    def get_bucket_policies(self):

        sr = self.session.resource(self.__class__.__name__.lower())

        for bucket in self.get("AWS::S3::Bucket").get("Resource"):
            try:

                bucket.set("Policy", json.loads(sr.BucketPolicy(
                    bucket.get('Name')).policy))
            except:  # no policy for this bucket
                pass

    def get_bucket_acls(self):

        sr = self.session.resource(self.__class__.__name__.lower())

        for bucket in self.get("AWS::S3::Bucket").get("Resource"):
            try:
                bucket.set("ACL", sr.BucketAcl(bucket.get('Name')).grants)
            except ClientError as e:
                if "AccessDenied" in str(e):
                    print(
                        f"Access denied when getting ACL for {bucket.get('Name')}")


class Lambda(Ingestor):
    run = [
        'functions',
        # 'layers'
    ]

    def __init__(self, session, account="0000000000000", only_types=[], except_types=[], only_arns=[], except_arns=[]):

        super().__init__(session=session, default=False)
        if not (super()._resolve_type_selection(only_types, except_types)
                and super()._resolve_arn_selection(only_arns, except_arns)):
            return

        self.client = self.session.client('lambda')

        for rt in self.run:

            print(f"{self.__class__.__name__}: Loading {rt}")

            resources = self._get_paginated(rt)

            for resource in resources:

                resource_type = rt.capitalize()[0:-1]
                properties = resource

                label = "AWS::%s::%s" % (
                    self.__class__.__name__.capitalize(),
                    resource_type.replace("Info", "").replace("Version", "").replace("Summary", ""))

                keys = [re.sub("^" + resource_type, "", k)
                        for k in properties.keys()]

                key = "%sArn" % resource_type
                properties["Arn"] = properties[key]
                del properties[key]

                key = "%sName" % resource_type
                properties["Name"] = properties[key]
                del properties[key]

                print(
                    f"{self.__class__.__name__}: Loading {properties['Arn']}")

                r = Resource(labels=[label], properties=properties)
                if r not in self:
                    self.append(r)

    def _get_paginated(self, resource_type):

        rs = [r for r in self.client.get_paginator(
            f"list_{resource_type}"
        ).paginate()]

        full = []

        for i in rs:
            full.extend(i[resource_type.capitalize()])

        return full
