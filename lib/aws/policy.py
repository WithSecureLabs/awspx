
import copy
import json
import re
from functools import reduce

from lib.aws.actions import ACTIONS
from lib.aws.resources import RESOURCES

from lib.graph.base import Element, Elements
from lib.graph.edges import Action, Trusts
from lib.graph.nodes import Resource, External

from lib.util.console import console


''' Consists of Principals, Actions, Resources, and Conditions '''


class Statement:

    _principals = None
    _actions = None
    _resources = None
    _conditions = None

    __statement = {}
    __resources = Elements()

    def __init__(self, statement, resource, resources):

        self.__statement = copy.deepcopy(statement)
        self.__resources = resources

        self.__str__ = lambda: str(statement)

        assert isinstance(self.__statement, dict)

        keys = [k for k in self.__statement.keys()]

        if not ("Effect" in keys
                and any([k in keys for k in ["Action", "NotAction"]])):

            console.critical(f"Statement: {self.__statement} "
                             "is missing required key")

        if "NotPrincipal" in keys:
            console.warn("'NotPrincipal' support hasn't been implemented."
                         f"Statement: {self.__statement} will be ignored.")

        elif "Principal" not in keys:
            self.__statement["Principal"] = {"AWS": [str(resource)]}
            self._principals = Elements([resource])

        if (not any([k in keys for k in ["Resource", "NotResource"]])
                and resource is not None):
            self.__statement["Resource"] = [str(resource)]
            self._resources = Elements([resource])

    def _get_principals(self):
        '''https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html'''

        principals = Elements()

        key = list(filter(lambda x: "Principal" in x,
                          self.__statement.keys()))[0]

        statement = self.__statement[key]

        if isinstance(statement, str) and statement == "*":
            statement = {"AWS": "*"}

        assert isinstance(statement, dict)

        if "AWS" in statement:

            if not isinstance(statement["AWS"], list):
                statement["AWS"] = [statement["AWS"]]

            if '*' in statement["AWS"]:

                external = External(
                    key="Arn",
                    labels=["AWS::Account"],
                    properties={
                        "Name": "All AWS Accounts",
                        "Description": "Pseudo-Account representing anyone who possesses an AWS account",
                        "Arn": "arn:aws:iam::{Account}:root"
                    })

                principals = Elements([*self.__resources.get('AWS::Iam::User').get("Resource"),
                                       *self.__resources.get('AWS::Iam::Role').get("Resource"),
                                       external])

            for principal in [p for p in statement["AWS"] if '*' not in statement["AWS"]]:

                if '*' in principal:
                    continue

                node = next((a for a in self.__resources.get("Resource")
                             if a.id() == principal),
                            None)

                # We haven't seen this node before. It may belong to another account,
                # or it belongs to a service that was not loaded.
                if node is None:

                    name = principal
                    labels = ["AWS::Account"]

                    if re.compile(f"^{RESOURCES.regex['Account']}$"
                                  ).match(principal) is not None:

                        principal = f"arn:aws:iam::{principal}:root"
                        labels += ["AWS::Account"]

                    elif re.compile(f"^arn:aws:iam::{RESOURCES.regex['Account']}:root$"
                                    ).match(principal) is not None:

                        name = str(principal.split(":")[4])
                        labels += ["AWS::Account"]

                    else:

                        for k, v in RESOURCES.items():

                            if re.compile(v).match(principal):
                                name = principal.replace(
                                    '/', ':').split(':')[-1]
                                labels = [k]
                                break

                    node = External(
                        key=str("Arn" if principal.startswith("arn")
                                else "CanonicalUser"),
                        labels=labels,
                        properties={
                            "Name": str(name),
                            str("Arn" if principal.startswith("arn") else "CanonicalUser"): principal,
                        })

                principals.add(node)

        elif "Service" in statement:

            services = statement["Service"] if isinstance(
                statement["Service"], list) else [statement["Service"]]

            for service in services:

                if service.lower().endswith("amazonaws.com"):
                    labels = ["AWS::Domain"]
                else:
                    labels = ["Internet::Domain"]

                principals.add(External(
                    key="Name",
                    labels=labels,
                    properties={
                        "Name": service
                    }))

        elif "Federated" in statement:

            node = None
            labels = []

            statements = statement["Federated"] \
                if isinstance(statement["Federated"], list) \
                else [statement["Federated"]]

            for federated in statements:

                if re.compile(
                    RESOURCES["AWS::Iam::SamlProvider"]
                ).match(federated) is not None:

                    base = Resource if (next((a for a in self.__resources.get("Resoure")
                                              if a.account() == federated.split(':')[4]
                                              ), False)) else External
                    node = base(
                        key="Arn",
                        labels=["AWS::Iam::SamlProvider"],
                        properties={
                            "Name": federated.split('/')[-1],
                            "Arn":  federated
                        })

                elif re.compile(
                    "^(?=.{1,253}\.?$)(?:(?!-|[^.]+_)[A-Za-z0-9-_]{1,63}(?<!-)(?:\.|$)){2,}$"
                ).match(federated):
                    node = External(
                        key="Name",
                        labels=["Internet::Domain"],
                        properties={
                            "Name": federated
                        })

                else:
                    node = External(
                        key="Name",
                        properties={
                            "Name": federated,
                        })
                principals.add(node)

        # TODO:
        elif "CanonicalUser" in statement:

            principals.add(External(
                key="CanonicalUser",
                labels=["AWS::Account"],
                properties={
                    "Name": statement["CanonicalUser"],
                    "CanonicalUser": statement["CanonicalUser"],
                }))

        else:
            console.warn("Unknown principal: ", statement)

        return principals

    def _get_actions(self):

        actions = set()
        key = list(filter(lambda x: "Action" in x,
                          self.__statement.keys()))[0]
        statement = self.__statement[key] if isinstance(
            self.__statement[key], list) else [self.__statement[key]]

        for action in [a for a in statement if '*' not in statement]:

            if '*' in action:
                actions.update(set(filter(
                    re.compile(action.replace("*", "(.*)")).match,
                    ACTIONS.keys())))
            else:
                actions.update([action] if action in ACTIONS.keys() else [])

        if '*' in statement and key != 'NotAction':
            actions = set(ACTIONS.keys())

        elif '*' in statement:
            actions = set()

        elif key == "NotAction":

            actions = [action for action in ACTIONS
                       if action not in actions]

        return sorted(list(actions))

    def _get_resources_and_conditions(self):

        resources = Elements()
        conditions = {}

        all_resources = self.__resources

        key = list(filter(lambda x: "Resource" in x,
                          self.__statement.keys()))[0]

        statement = self.__statement[key] \
            if isinstance(self.__statement[key], list) \
            else [self.__statement[key]]

        for rlp in set([r.replace('*', "(.*)") + "$" for r in statement
                        if '*' not in statement and len(all_resources) > 0
                        ]):

            # Identify variable resource-level permissions
            variables = list(re.findall("\$\{[0-9a-zA-Z:]+\}", rlp))
            regex = re.compile(reduce(lambda x, y: x.replace(y, "(.*)"),
                                      variables, rlp))

            # Match resource-level permissions against resource arns
            results = Elements(filter(lambda r: regex.match(r.id()),
                                      all_resources))

            # Standard case: add results to result set
            if len(variables) == 0:
                for r in results:
                    conditions[r.id()] = [{}]
                    resources.add(r)

            offset = len([x for x in rlp if x == '(']) + 1

            # Handle resource-level permissions
            for result in [r for r in results
                           if r.id() not in conditions
                           or conditions[r.id()] != [{}]]:

                # TODO: skip resources that incorporate contradictory conditions
                condition = {
                    "StringEquals": {
                        variables[i]: regex.match(
                            result.id()).group(offset + i)
                        for i in range(len(variables))}
                }

                if result.id() not in conditions:
                    conditions[result.id()] = []

                if condition not in conditions[result.id()]:
                    conditions[result.id()].append(condition)

                if result not in resources:
                    resources.add(result)

        if '*' in statement:

            resources = all_resources

        elif key == "NotResource":
            resources = [r for r in all_resources
                         if r not in resources]

        resources = Elements(resources)
        conditions = {str(r): conditions[r.id()] if r.id() in conditions else [{}]
                      for r in resources}

        return (resources, conditions)

    def principals(self):

        if self._principals is None:
            self._principals = self._get_principals()

        return self._principals

    def actions(self):

        if self._actions is not None:
            return self._actions

        (principals, actions, resources, conditions) = (self.principals(),
                                                        Elements(),
                                                        self.resources(),
                                                        self.conditions())

        for action in self._get_actions():

            action_resources = Elements()

            # Actions that do not affect specific resource types.
            if ACTIONS[action]["Affects"] == {}:
                action_resources.update(Elements(
                    self.__resources.get("CatchAll")))

            for affected_type in ACTIONS[action]["Affects"].keys():
                # Ignore mutable actions affecting built in policies
                if (affected_type == "AWS::Iam::Policy" and ACTIONS[action]["Access"] in [
                    "Permissions Management",
                    "Write"
                ]):
                    action_resources.update([a for a in resources.get(affected_type)
                                             if str(a).split(':')[4] != "aws"])
                else:
                    action_resources.update(
                        resources.get(affected_type)
                    )

            for resource in action_resources:
                # Action conditions comprise of resource-level conditions and statement conditions
                resource_conditions = list(conditions[str(resource)]
                                           if str(resource) in conditions else [{}])

                statement_conditions = dict(self.__statement["Condition"]
                                            if "Condition" in self.__statement.keys() else {})
                # Add the two together
                condition = json.dumps([
                    {
                        **resource_conditions[i],
                        **statement_conditions
                    } for i in range(len(resource_conditions))
                ]) if (len(resource_conditions[0]) + len(statement_conditions)) > 0  \
                    else "[]"

                # Incorporate all items from ACTIONS.py
                supplementary = next((ACTIONS[action]["Affects"][r]
                                      for r in resource.labels()
                                      if r in ACTIONS[action]["Affects"]),
                                     {})

                for principal in self._principals:

                    actions.add(Action(
                        properties={
                            "Name":         action,
                            "Description":  ACTIONS[action]["Description"],
                            "Effect":       self.__statement["Effect"],
                            "Access":       ACTIONS[action]["Access"],
                            "Reference":    ACTIONS[action]["Reference"],
                            "Condition":    condition,
                            **supplementary
                        }, source=principal, target=resource))

        # Unset resource level permission conditions
        for resource in self._resources:
            resource.condition = []

        self._actions = actions

        return self._actions

    def resources(self):

        if self._resources is None:
            (self._resources, self._conditions) = self._get_resources_and_conditions()

        return self._resources

    def conditions(self):

        if self._conditions is None:
            (self._resources, self._conditions) = self._get_resources_and_conditions()

        return self._conditions


''' Consists of one or more Statements '''


class Document:

    def __init__(self, document, resource, resources):

        self.statements = []

        if not (isinstance(document, dict)
                and "Version" in document
                and document["Version"] == "2012-10-17"
                and "Statement" in document):
            return

        self.document = json.loads(json.dumps(document))

        if not isinstance(self.document["Statement"], list):
            self.document["Statement"] = [self.document["Statement"]]

        for statement in self.document["Statement"]:
            self.statements.append(Statement(statement=statement,
                                             resource=resource,
                                             resources=resources))

    def __len__(self):
        return len(self.statements)

    def principals(self):

        principals = Elements()

        for statement in self.statements:
            principals.update(statement.principals())

        return principals

    def actions(self):

        actions = Elements()

        for statement in self.statements:
            actions.update(statement.actions())

        return actions


''' Consists of one or more Documents '''


class Policy:

    def __init__(self, resource, resources):

        self.__resource = resource
        self.documents = {}

    def __len__(self):
        return len(self.documents)

    def principals(self):

        principals = Elements()

        for policy in self.documents.values():
            principals.update(policy.principals())

        return principals

    def actions(self):

        actions = Elements()

        for document in self.documents.values():
            actions.update(document.actions())

        console.info(f"{self.__class__.__name__} {self.__resource} "
                     f"resolved to {len(actions)} Action(s)")

        return actions


''' Inline and Managed Policies associated with IAM entities '''


class IdentityBasedPolicy(Policy):

    def __init__(self, resource, resources):

        super().__init__(resource, resources)

        key = list(filter(lambda k: k == "Document" or k == "Documents",
                          resource.properties().keys()))
        if len(key) != 1:
            return

        # Set self.documents
        for policy in resource.properties()[key[0]]:
            for name, document in policy.items():
                self.documents[name] = Document(document, resource, resources)


''' Policies that define actions permitted to be performed on the associated resource. '''


class ResourceBasedPolicy(Policy):

    # https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html

    def __init__(self, resource, resources, keys=[]):

        super().__init__(resource, resources)

        for k, v in resource.properties().items():

            if not (len(keys) == 0 or k in keys):
                continue

            document = Document(v, resource, resources)

            if not len(document) > 0:
                continue

            # Set self.documents
            self.documents[k] = Document(resource.properties()[k],
                                         resource, resources)


''' Resource based policy variant, specific to S3 Buckets and their Objects '''


class BucketACL(ResourceBasedPolicy):
    # https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#specifying-grantee

    AccessControlList = {
        "READ": [
            "s3:ListBucket",
            "s3:ListBucketVersions",
            "s3:ListBucketMultipartUploads"
        ],
        "WRITE": [
            "s3:PutObject",
            "s3:DeleteObject"
        ],
        "READ_ACP": [
            "s3:GetBucketAcl"
        ],
        "WRITE_ACP": [
            "s3:PutBucketAcl"
        ],
        "FULL_CONTROL": [
            "s3:DeleteObject",
            "s3:GetBucketAcl",
            "s3:ListBucket",
            "s3:ListBucketMultipartUploads",
            "s3:ListBucketVersions",
            "s3:PutBucketAcl",
            "s3:PutObject"
        ],
    }

    def __init__(self, resource, resources):

        statements = []

        for key, acls in resource.properties().items():

            # Property is not a valid ACL
            if not (isinstance(acls, list)
                    and all(["Grantee" in x and "Permission" for x in acls])):
                continue

            # Construct a policy from ACL
            for (grantee, permission) in map(lambda x: (x["Grantee"], x["Permission"]), acls):

                statement = {
                    "Effect": "Allow"
                }

                # Handle Principal
                if grantee["Type"] not in ["CanonicalUser", "Group"]:
                    raise ValueError

                if grantee["Type"] == "CanonicalUser":

                    statement["Principal"] = {"CanonicalUser": grantee["ID"]}

                elif grantee["Type"] == "Group":

                    group = grantee["URI"].split('/')[-1]

                    # Any AWS account can access this resource
                    if group == "AuthenticatedUsers":
                        statement["Principal"] = {"AWS": "*"}

                    # Anyone (not neccessarily AWS)
                    elif group == "AllUsers":
                        statement["Principal"] = {"AWS": "*"}

                    # Service
                    elif group == "LogDelivery":
                        statement["Principal"] = {"Service": grantee["URI"]}

                    # Specific AWS resource
                    else:
                        statement["Principal"] = {"AWS": grantee["URI"]}

                # Handle Actions
                statement["Action"] = self.AccessControlList[permission]

                # Handle Resources (Bucket and Objects in Bucket)
                statement["Resource"] = [resource.id(), resource.id() + "/*"]

                statements.append(statement)

        if len(statements) > 0:

            resource.properties()["_"] = {
                "Version": "2012-10-17",
                "Statement": statements
            }

        super().__init__(resource, resources, keys=["_"])

        if "_" in resource.properties():
            del resource.properties()["_"]


class ObjectACL(BucketACL):
    # https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#specifying-grantee

    AccessControlList = {
        "READ": [
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:GetObjectTorrent"
        ],
        "WRITE": [
        ],
        "READ_ACP": [
            "s3:GetObjectAcl",
            "s3:GetObjectVersionAcl",
        ],
        "WRITE_ACP": [
            "s3:PutObjectAcl",
            "s3:PutObjectVersionAcl",
        ],
        "FULL_CONTROL": [
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:GetObjectTorrent",
            "s3:GetObjectAcl",
            "s3:GetObjectVersionAcl",
            "s3:PutObjectAcl",
            "s3:PutObjectVersionAcl",
        ],
    }
