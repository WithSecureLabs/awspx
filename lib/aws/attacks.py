
import copy
import json
import re
import time

from lib.graph.db import Neo4j

definitions = {

    "CreatePolicyVersion": {

        "Description": "Overwrite the default version of the target managed policy:",

        "Commands": [
            "aws create-policy-version"
            "   --policy-arn ${AWS::Iam::Policy.Arn}"
            "   --set-as-default"
            "   --policy-document file://<(cat <<EOF\n"
            "{\n"
            "    \"Version\": \"2012-10-17\",\n"
            "    \"Statement\": [\n"
            "        {\n"
            "            \"Sid\": \"Admin\",\n"
            "            \"Effect\": \"Allow\",\n"
            "            \"Action\": \"*\",\n"
            "            \"Resource\": \"*\"\n"
            "        }]\n"
            "}\n"
            "EOF\n"
            ")"
        ],

        "Attack": {

            "Depends": "AWS::Iam::Policy",

            "Requires": [
                "iam:CreatePolicyVersion"
            ],

            "Affects": "AWS::Iam::Policy",

            "Grants": "Admin"

        }
    },

    "AssociateInstanceProfile": {

        "Description": "Associate the specified EC2 instance with the target instance profile: ",

        "Commands": [
            "aws ec2 associate-iam-instance-profile"
            "   --instance-id ${AWS::Ec2::Instance}"
            "   --iam-instance-profile Name=${AWS::Iam::InstanceProfile}"
        ],

        "Attack": {

            "Depends": "AWS::Ec2::Instance",

            "Requires": [
                "ec2:AssociateIamInstanceProfile"
            ],

            "Affects": "AWS::Ec2::Instance",

            "Grants": "AWS::Iam::InstanceProfile",

            "Cypher": [
                # The instance profile doesnt exist or it can be deleted indirectly
                "(NOT EXISTS((${AWS::Ec2::Instance})-[:TRANSITIVE]->(:`AWS::Iam::InstanceProfile`))",
                "   OR EXISTS((${})-[:I|ACTION{Name:'ec2:DisassociateIamInstanceProfile'}]->(${AWS::Ec2::Instance}))",
                # The instance profile has no role or iam:Pass role can be performed
                ") AND (NOT EXISTS((${AWS::Iam::InstanceProfile})-[:TRANSITIVE]->(:`AWS::Iam::Role`))",
                "OR EXISTS((${})-[:D|ACTION{Name:'iam:PassRole'}]->(:`AWS::Iam::Role`)<-[:TRANSITIVE]-(${AWS::Iam::InstanceProfile})))"
            ]

        }
    },

    "AssumeRole": {

        "Description": "Retrieve a set of temporary security credentials from assuming the target role:",

        "Commands": [
            "aws sts assume-role"
            "   --role-arn ${AWS::Iam::Role.Arn}"
            "   --role-session-name AssumeRole"
        ],

        "Attack": {

            "Requires": [
                "sts:AssumeRole"
            ],

            "Affects": "AWS::Iam::Role",

            "Cypher": [
                "(${})<-[:TRUSTS{Name:'sts:AssumeRole'}]-(${AWS::Iam::Role})"
            ]

        }
    },

    "AddRoleToInstanceProfile": {

        "Description": "Add the target role to the specified instance profile:",

        "Commands": [
            "aws iam add-role-to-instance-profile"
            "   --instance-profile-name ${AWS::Iam::InstanceProfile}"
            "   --role-name ${AWS::Iam::Role}"
        ],

        "Attack": {

            "Depends": "AWS::Iam::InstanceProfile",

            "Requires": [
                "iam:AddRoleToInstanceProfile"
            ],

            "Affects": "AWS::Iam::InstanceProfile",

            "Grants": "AWS::Iam::Role",

            "Cypher": [
                # EC2 is trusted by the role
                "(EXISTS((${AWS::Iam::Role})-[:TRUSTS]->({Name:'ec2.amazonaws.com'}))",
                # The instance profile has no role or it can be detached
                "AND EXISTS((${})-[:I|ACTION{Name:'iam:RemoveRoleFromInstanceProfile'}]->(${AWS::Iam::InstanceProfile}))",
                "   OR NOT EXISTS((${AWS::Iam::InstanceProfile})-[:TRANSITIVE]->(${AWS::Iam::Role})))"
            ]
        }
    },

    "AddUserToGroup": {

        "Description": "Add the specified user to the target group:",

        "Commands": [
            "aws iam add-user-to-group"
            "   --group-name ${AWS::Iam::Group}"
            "   --user-name ${AWS::Iam::User}"
        ],

        "Attack": {

            "Depends": "AWS::Iam::User",

            "Requires": [
                "iam:AddUserToGroup"
            ],

            "Affects": "AWS::Iam::Group"

        }
    },

    "AttachGroupPolicy": {

        "Description": "Attach the target managed policy to the specified group:",

        "Commands": [
            "aws iam attach-group-policy"
            "   --group-name ${AWS::Iam::Group}"
            "   --policy-arn ${AWS::Iam::Policy.Arn}"
        ],

        "Attack": {

            "Depends": "AWS::Iam::Group",

            "Requires": [
                "iam:AttachGroupPolicy",
            ],

            "Affects": "AWS::Iam::Group",

            "Grants": "AWS::Iam::Policy"

        }
    },

    "AttachRolePolicy": {

        "Description": "Attach the target managed policy to the specified role:",

        "Commands": [
            "aws iam attach-role-policy"
            "   --role-name ${AWS::Iam::Role}"
            "   --policy-arn ${AWS::Iam::Policy.Arn}"
        ],

        "Attack": {

            "Depends": "AWS::Iam::Role",

            "Requires": [
                "iam:AttachRolePolicy"
            ],

            "Affects": "AWS::Iam::Role",

            "Grants": "AWS::Iam::Policy"
        }

    },

    "AttachUserPolicy": {

        "Description": "Attach the target managed policy to the specified user:",

        "Commands": [
            "aws iam attach-user-policy"
            "   --user-name ${AWS::Iam::User}"
            "   --policy-arn ${AWS::Iam::Policy.Arn}"
        ],

        "Attack": {

            "Depends": "AWS::Iam::User",

            "Requires": [
                "iam:AttachUserPolicy",
            ],

            "Affects": "AWS::Iam::User",

            "Grants": "AWS::Iam::Policy"

        }
    },

    "CreateGroup": {

        "Description": "Create a new group and add the specified user to it:",

        "Options": {
            "CreateAction": True,
            "Transitive": False
        },

        "Commands": [
            "aws iam create-group --group-name ${AWS::Iam::Group}"
        ],

        "Attack": {

            "Requires": [
                "iam:CreateGroup"
            ],

            "Affects": "AWS::Iam::Group"

        },
    },

    "CreateInstance": {

        "Description": "Launch a new EC2 instance:",

        "Options": {
            "CreateAction": True,
            "Transitive": True
        },

        "Commands": [
            "aws ec2 run-instances"
            "   --count 1"
            "   --instance-type t2.micro"
            "   --image-id $AmiId",
        ],

        "Attack": {

            "Requires": [
                "ec2:RunInstances"
            ],

            "Affects": "AWS::Ec2::Instance",

        }
    },

    "CreateInstanceProfile": {

        "Description": "Create a new instance profile:",

        "Options": {
            "CreateAction": True,
            "Transitive": False
        },

        "Commands": [
            "aws iam create-instance-profile"
            "   --instance-profile-name ${AWS::Iam::InstanceProfile}"
        ],


        "Attack": {

            "Requires": [
                "iam:CreateInstanceProfile"
            ],

            "Affects": "AWS::Iam::InstanceProfile",

        }
    },

    "CreatePolicy": {

        "Description": "Create a new managed policy:",

        "Options": {
            "CreateAction": True,
            "Transitive": False
        },

        "Commands": [
            "aws iam create-policy"
            "   --policy-name ${AWS::Iam::Policy}"
            "   --policy-document file://<(cat <<EOF\n"
            "{\n"
            "    \"Version\": \"2012-10-17\",\n"
            "    \"Statement\": [\n"
            "        {\n"
            "            \"Sid\": \"Admin\",\n"
            "            \"Effect\": \"Allow\",\n"
            "            \"Action\": \"*\",\n"
            "            \"Resource\": \"*\"\n"
            "        }]\n"
            "}\n"
            "EOF\n"
            ")"
        ],

        "Attack": {

            "Requires": [
                "iam:CreatePolicy",
            ],

            "Affects": "AWS::Iam::Policy",

            "Grants": "Admin"
        },
    },

    "CreateRole": {

        "Description": [
            "Create a new role to assume:",
            "Retrieve a set of temporary security credentials from assuming the target role:"
        ],

        "Options": {
            "CreateAction": True,
            "Transitive": True
        },

        "Commands": [
            "aws iam create-role"
            "   --role-name ${AWS::Iam::Role} "
            "   --assume-role-policy-document file://<(cat <<EOF\n"
            "{\n"
            "  \"Version\": \"2012-10-17\",\n"
            "  \"Statement\": [\n"
            "    {\n"
            "      \"Effect\": \"Allow\",\n"
            "      \"Action\": \"sts:AssumeRole\",\n"
            "      \"Principal\": {\n"
            "        \"AWS\": \"*\"\n"
            "      }\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "EOF\n"
            ")",
            "aws sts assume-role"
            "   --role-arn ${AWS::Iam::Role.Arn}"
            "   --role-session-name AssumeRole"
        ],

        "Attack": {

            "Requires": [
                "iam:CreateRole",
            ],

            "Affects": "AWS::Iam::Role",

        }

    },

    "CreateUser": {

        "Description": "Create a new user:",

        "Options": {
            "CreateAction": True,
            "Transitive": False
        },

        "Commands": [
            "aws iam create-user --user-name ${AWS::Iam::User}",
        ],

        "Attack": {

            "Requires": [
                "iam:CreateUser"
            ],

            "Affects": "AWS::Iam::User"

        }
    },

    "PutGroupPolicy": {

        "Description": "Add a new administrative inline policy document to the target group:",

        "Commands": [
            "aws iam put-group-policy"
            "   --group-name ${AWS::Iam::Group}"
            "   --policy-name Admin"
            "   --policy-document file://<(cat <<EOF\n"
            "{\n"
            "    \"Version\": \"2012-10-17\",\n"
            "    \"Statement\": [\n"
            "        {\n"
            "            \"Sid\": \"Admin\",\n"
            "            \"Effect\": \"Allow\",\n"
            "            \"Action\": \"*\",\n"
            "            \"Resource\": \"*\"\n"
            "        }]\n"
            "}\n"
            "EOF\n"
            ")"
        ],

        "Attack": {

            "Depends": "AWS::Iam::Group",

            "Requires": [
                "iam:PutGroupPolicy"
            ],

            "Affects": "AWS::Iam::Group",

            "Grants": "Admin"

        },
    },

    "PutRolePolicy": {

        "Description": "Add a new administrative inline policy document to the target role:",

        "Commands": [
            "aws iam put-role-policy"
            "   --role-name ${AWS::Iam::Role}"
            "   --policy-name Admin"
            "   --policy-document file://<(cat <<EOF\n"
            "{\n"
            "    \"Version\": \"2012-10-17\",\n"
            "    \"Statement\": [\n"
            "        {\n"
            "            \"Sid\": \"Admin\",\n"
            "            \"Effect\": \"Allow\",\n"
            "            \"Action\": \"*\",\n"
            "            \"Resource\": \"*\"\n"
            "        }]\n"
            "}\n"
            "EOF\n"
            ")"
        ],

        "Attack": {

            "Depends": "AWS::Iam::Role",

            "Requires": [
                "iam:PutRolePolicy"
            ],

            "Affects": "AWS::Iam::Role",

            "Grants": "Admin"

        },
    },

    "PutUserPolicy": {

        "Description": "Add a new administrative inline policy document to the target user:",

        "Commands": [
            "aws iam put-user-policy"
            "   --user-name ${AWS::Iam::User}"
            "   --policy-name Admin "
            "   --policy-document file://<(cat <<EOF\n"
            "{\n"
            "    \"Version\": \"2012-10-17\",\n"
            "    \"Statement\": [\n"
            "        {\n"
            "            \"Sid\": \"Admin\",\n"
            "            \"Effect\": \"Allow\",\n"
            "            \"Action\": \"*\",\n"
            "            \"Resource\": \"*\"\n"
            "        }]\n"
            "}\n"
            "EOF\n"
            ")"
        ],

        "Attack": {

            "Depends": "AWS::Iam::User",

            "Requires": [
                "iam:PutUserPolicy"
            ],

            "Affects": "AWS::Iam::User",

            "Grants": "Admin"

        },
    },

    "UpdateRole": {

        "Description": [
            "Update the assume-role policy document of the target role and assume it thereafter:",
            "Retrieve a set of temporary security credentials from assuming the target role:"
        ],

        "Commands": [
            "aws iam update-assume-role-policy"
            "   --role-name ${AWS::Iam::Role}"
            "   --policy-document file://<(cat <<EOF\n"
            "{\n"
            "  \"Version\": \"2012-10-17\",\n"
            "  \"Statement\": [\n"
            "    {\n"
            "      \"Effect\": \"Allow\",\n"
            "      \"Action\": \"sts:AssumeRole\",\n"
            "      \"Principal\": {\n"
            "        \"AWS\": \"*\"\n"
            "      }\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "EOF\n"
            ")",

            "aws sts assume-role"
            "   --role-arn ${AWS::Iam::Role.Arn}"
            "   --role-session-name AssumeRole"
        ],

        "Attack": {

            "Requires": [
                "iam:UpdateAssumeRolePolicy"
            ],

            "Affects": "AWS::Iam::Role"

        }
    },

    "UpdateLoginProfile": {

        "Description": "Reset the target user's console password and login as them:",

        "Commands": [
            "aws iam update-login-profile"
            "   --user-name ${AWS::Iam::User}"
            "   --password $Password"
        ],

        "Attack": {

            "Requires": [
                "iam:UpdateLoginProfile"
            ],

            "Affects": "AWS::Iam::User"

        }
    },

    "CreateLoginProfile": {

        "Description": "Set a console password for the target user and login as them, nothing has been set before:",

        "Commands": [
            "aws iam create-login-profile"
            "   --user-name ${AWS::Iam::User}"
            "   --password $Password"
        ],

        "Attack": {

            "Requires": [
                "iam:CreateLoginProfile"
            ],

            "Affects": "AWS::Iam::User",

            "Cypher": [
                "(${AWS::Iam::User.LoginProfile} IS NULL",
                "OR EXISTS((${})-[:I|ACTION{Name:'iam:DeleteLoginProfile'}]->(${AWS::Iam::User})))"
            ]
        }
    },

    "CreateAccessKey": {

        "Description": "Create an access key for the target user and authenticate as them using the API:",

        "Commands": [
            "aws iam create-access-key --user-name ${AWS::Iam::User}"
        ],

        "Attack": {

            "Requires": [
                "iam:CreateAccessKey"
            ],

            "Affects": "AWS::Iam::User",

            "Cypher": [
                "((COALESCE(SIZE(SPLIT(${AWS::Iam::User.AccessKeys},'Status')), 1) - 1) < 2",
                "OR EXISTS((${})-[:I|ACTION{Name:'iam:DeleteAccessKey'}]->(${AWS::Iam::User})))"
            ]

        }
    }

}


class Attacks:

    definitions = definitions
    stats = []

    def __init__(self, skip_attacks=[], only_attacks=[],
                 skip_conditional_actions=True, max_search_depth="",
                 console=None
                 ):

        if console is None:
            from lib.util.console import console

        self.console = console
        self.conditional = skip_conditional_actions

        self.definitions = {k: self.definitions[k]
                            for k in list(self.definitions.keys()
                                          if only_attacks == []
                                          else only_attacks)
                            if k not in skip_attacks
                            }
        self.queries = {k: self.translate(k, max_search_depth)
                        for k, v in self.definitions.items()
                        }

    def translate(self, name, max_search_depth=""):

        definition = self.definitions[name]
        attack = definition["Attack"]
        cypher = str()

        strings = {
            "name": name,
            "description": list([definition["Description"]]
                                if isinstance(definition["Description"], str)
                                else definition["Description"]),

            "commands": definition["Commands"],
            "requires": attack["Requires"],
            "affects": attack["Affects"],

            "depends": str(attack["Depends"]
                           if "Depends" in attack
                           else ""),
            "grants": str(attack["Grants"]
                          if "Grants" in attack
                          else ""),

            "depth": max_search_depth,
            "size": len(attack["Requires"]),
        }

        options = {
            "AffectsGeneric": False,
            "CreateAction": False,
            "Transitive": True,
            "Admin": bool(True
                          if "Grants" in attack
                          and attack["Grants"] == "Admin"
                          else False),
            ** dict(definition["Options"]
                    if "Options" in definition
                    else {}),
        }

        def cypher_resolve_commands(history=False):

            # A nested REPLACE operation must occur for every placeholder in the format string.
            # Resolution occurs by performing a type comparison against fields in the pattern's
            # definition.

            resolved = "_"

            for (placeholder, attr) in sorted(
                    re.findall(r"\$\{(AWS\:\:[A-Za-z0-9]+\:\:[A-Za-z0-9]+)?(\.[A-Za-z]+)?\}",
                               ';'.join(strings["commands"])
                               ),
                    key=lambda x: len(x[0]+x[1]),
                    reverse=True):

                substitute = None

                if placeholder == attack["Affects"]:
                    substitute = "grant" if "Grants" not in attack else "option"

                elif ("Depends" in attack
                      and placeholder == attack["Depends"]):
                    substitute = "option"

                elif ("Grants" in attack
                      and placeholder == attack["Grants"]):
                    substitute = "grant"

                elif placeholder == '':
                    substitute = "source"

                else:
                    self.console.error(f"Unknown placeholder: '{placeholder}'")
                    continue

                if len(attr) == 0:
                    substitute += ".Name"

                else:
                    substitute += attr
                    placeholder += attr

                resolved = f"REPLACE({resolved}, \"${{{placeholder}}}\", {substitute})"

            resolved = ("[_ IN %s|%s]" % (strings["commands"], resolved)
                        ).replace('{', '{{').replace('}', '}}')

            if history:

                resolved = (
                    "REDUCE(commands=[], _ IN history + %s|"
                    "CASE WHEN _ IN commands THEN commands "
                    "ELSE commands + _ END) "
                    "AS commands") % (resolved)

            else:
                resolved += " AS commands"

            return resolved

        def cypher_resolve_placeholder(placeholder):

            if placeholder == "":
                return "source"

            elif placeholder == attack["Affects"]:
                return "target"

            elif ("Depends" in attack
                  and placeholder == attack["Depends"]):
                return "option"

            elif ("Grants" in attack
                  and placeholder == attack["Grants"]):
                return "grant"

            else:
                r = re.compile(r"(AWS::[A-Za-z0-9:]+)"
                               ).match(placeholder)

                if r.group(1) is not None:
                    return str(f"{r.group(1).replace(':', '').lower()}"
                               f":`{r.group(1)}`")

        def cypher_inject():

            inject = ' '.join(attack["Cypher"])
            retain = ["source", "edge", "options", "target",
                      "path", "grants", "admin"
                      ]

            unwound = []

            for k, v in {
                    k: cypher_resolve_placeholder(k) for k in set([
                        r for (r, _) in re.findall(
                            r"\$\{(AWS\:\:[A-Za-z0-9]+\:\:[A-Za-z0-9]+)?(\.[A-Za-z]+)?\}",
                            inject
                        )
                    ])}.items():

                if (v not in unwound and v in ["option", "grant"]):
                    unwound.append(v)

                inject = re.sub(
                    rf"\${{{k}(?P<property>\.[a-zA-Z]+)?}}",
                    lambda x: (f"{v}{x.groupdict()['property']}"
                               if x.groupdict()['property'] is not None
                               else v),
                    inject)

            # Expand ACTION shorthand
            inject = re.sub(
                r"\[:((?P<directive>I|D)?\|)?(?P<type>ACTION|TRUSTS)(\{(?P<properties>[^}.]*)\})?\]",
                lambda x: ''.join([
                    str(  # D (Direct)
                        f"[:TRANSITIVE|ATTACK*0..{strings['depth']}]->()-" if x.groupdict()['directive'] == "I"
                        # I (Indirect)
                        else f"[:TRANSITIVE*0..{strings['depth']}]->()-" if x.groupdict()['directive'] == "D"
                        # None
                        else ""
                    ),
                    f"[:{x.groupdict()['type']}{{",
                    ', '.join([
                        f"{k}: '{v}'" for k, v in {"Effect": 'Allow',  # Default to allow
                                                   **dict({"Condition": []} if self.conditional else {}),
                                                   **{k: v for (k, v) in [
                                                       re.sub(r"[^\S]*(?P<k>[^:.]*):'(?P<v>[^'.]*)'",
                                                              lambda x: f"{x.groupdict()['k']},{x.groupdict()['v']}",
                                                              p).split(',')
                                                       for p in str(x.groupdict()["properties"]).split(",") if p != "None"
                                                   ]}
                                                   }.items()]),
                    "}]"
                ]),
                inject)

            if len(unwound) > 0:

                inject = " ".join((
                    "WITH " + ", ".join(retain),
                    " ".join(["UNWIND %s AS %s" % (i, i[:-1])
                              for i in retain
                              if i[:-1] in unwound
                              ]),
                    "WITH " + ", ".join([i
                                         if i[:-1] not in unwound
                                         else "{i}[0] AS {i}, {i}[1] AS _{i}".format(i=i[:-1])
                                         for i in retain
                                         ]),
                    "WHERE " + inject,  # Cypher injection point
                    "WITH " + ", ".join([i if i[:-1] not in unwound
                                         else "COLLECT([{i},_{i}]) AS {j}".format(i=i[:-1], j=i)
                                         for i in retain
                                         ])
                ))

            else:
                inject = "AND " + inject

            return re.sub("([{}]+)", lambda x: x.groups()[0] * 2, inject)

        # If a node, or edge, is identified to grant Admin, it is excluded from search.
        # This is because all patterns incorporating Admin are implied - searching further
        # would be redundant.

        cypher += (
            "OPTIONAL MATCH (admin)-[r:ATTACK|TRANSITIVE*0..]->(:Admin), "
            "   (default:Admin{{Arn:'arn:aws:iam::{{Account}}:policy/Admin'}}) "
            "   WHERE NOT (admin:Pattern OR admin:Admin) "
            "WITH COLLECT(DISTINCT COALESCE(admin, default)) AS admin, "
            "   [[NULL, []]] AS options, [NULL, []] AS grants "
        )

        # Patterns including a "Depends" value require an additional argument, which must
        # be reachable. This amounts to determining whether any nodes of that type can
        # be reached (transitively, or through performing one or more attacks).
        # Consequently, it must incorporate a weight that is computed once all required
        # commands have been consilidated. Dependencies need to be determined first to
        # avoid erroneous exclusion when deduplication is performed.

        if "Depends" in attack:

            strings["option_type"] = attack["Depends"]

            cypher += (
                "MATCH path=(source)-[:TRANSITIVE|ATTACK|CREATE*0..{depth}]->(option:`{option_type}`) "
                "   WHERE ALL(_ IN RELATIONSHIPS(path) WHERE TYPE(_) <> 'CREATE' OR _.Transitive) "
                "   AND NOT (source IN admin OR option IN NODES(path)[1..-1]) "
                "   AND (source:Resource OR source:External) AND (option:Resource OR option:Generic) "

                "WITH DISTINCT source, option, admin, "
                "   [_ IN RELATIONSHIPS(path) WHERE STARTNODE(_):Pattern] AS dependencies "

                "WITH admin, COLLECT([source, option, REDUCE("
                "   commands=[], _ IN dependencies|"
                "       CASE WHEN _ IN commands THEN commands "
                "       ELSE commands + _.Commands END)]"
                "   ) AS results "

                "UNWIND results AS result "

                "WITH admin, results, result[0] AS source, result[1] AS option, "
                "   MIN(SIZE(result[2])) AS weight "

                "UNWIND results AS result "
                "WITH admin, result, source, option, weight, result[2] AS commands "
                "   WHERE source = result[0] AND option = result[1] "
                "   AND weight = SIZE(result[2]) "

                "WITH admin, source, option, commands, weight ORDER BY weight "
                "WITH admin, source, COLLECT([option, commands]) AS options, [NULL, []] AS grants "
            )

        # No dependencies: source may be any Resource/External (excluding those known to grant Admin).

        else:

            cypher += (
                "MATCH (source) "
                "WHERE NOT source IN admin AND (source:Resource OR source:External) "

                "WITH admin, source, options, grants "
            )

        # Patterns including a "Grants" value grant transitivity to a resource type that may not the
        # affected type (e.g. iam:AttachGroupPolicy affects a group but grants transitivity to a policy).
        # The grants type can either be a resource or a creatable generic, reachable directly or indirectly.

        if "Grants" in attack:

            cypher += ''.join((

                "OPTIONAL MATCH (grant:`{grants}`) ",
                "   WHERE NOT grant:Generic ",
                "   AND grant:Resource " if attack["Grants"] != "Admin" else "",

                "OPTIONAL MATCH creation=shortestPath((source)-[:TRANSITIVE|ATTACK|CREATE*..{depth}]->(pattern:Pattern)), "
                "   (pattern)-[create:ATTACK]->(generic) "
                "   WHERE source <> pattern AND TYPE(REVERSE(RELATIONSHIPS(creation))[0]) = 'CREATE' "
                "       AND EXISTS((pattern)-[:OPTION|ATTACK]->(:`{grants}`)) ",

                "WITH DISTINCT source, options, admin, ",
                "grant, generic, REDUCE(commands=[], _ IN [",
                "   _ IN [_ IN RELATIONSHIPS(creation) ",
                "       WHERE STARTNODE(_):Pattern]|_.Commands]|",
                "   CASE WHEN _ IN commands THEN commands ",
                "   ELSE commands + _ END",
                "   ) + create.Commands AS commands ",

                "WITH source, options, admin, ",
                "COLLECT([grant, []]) + COLLECT([generic, commands]) AS grants ",
                "UNWIND grants AS grant ",

                "WITH DISTINCT source, options, admin, ",
                "grant[0] AS grant, grant[1] AS commands ",
                "WHERE grant[0] IS NOT NULL ",

                "WITH source, options, admin, ",
                "COLLECT([grant, commands]) AS grants ",
            ))

        # Assert: WITH options, grants, admin

        if (strings["size"] == 1 and "Depends" not in attack and "Cypher" not in attack):

            # If only one relationship is required, and there are no dependencies,
            # only direct relationships need to be identified, weight computation
            # and pruning requirements can be safely ommitted.

            cypher += ' '.join((
                "MATCH path=(source)-[edge:ACTION{{Name:'{requires[0]}', Effect: 'Allow'}}]"
                "->(target:`{affects}`) ",

                "WHERE NOT source:Pattern ",
                "   AND ALL(_ IN REVERSE(TAIL(REVERSE(NODES(path)))) WHERE NOT _ IN admin) ",
                "   AND edge.Condition = '[]' " if self.conditional else "",

                # target types that are dependant on being reachable transitively.
                '   AND target IN [_ IN options|_[0]] ' if ("Depends" in attack
                                                            and attack["Depends"] == attack["Affects"]) else "",

                cypher_inject() if "Cypher" in attack else "",

                "WITH  source, target, [] AS commands, options, grants, admin ",
            ))
        else:

            # Otherwise, the attack may incorporate indirect relationships (a dependency or
            # or a combination of one or more relationships.

            cypher += ' '.join((

                "MATCH path=(source)-[:TRANSITIVE|ATTACK*0..{depth}]->()-[edge:ACTION]->(target:`{affects}`)",
                "   WHERE NOT source:Pattern",
                "   AND ALL(_ IN REVERSE(TAIL(REVERSE(NODES(path)))) WHERE NOT _ IN admin)",
                "   AND edge.Name IN {requires} AND edge.Effect = 'Allow' ",
                "   AND edge.Condition = '[]' " if self.conditional else "",
                '   AND target IN [_ IN options|_[0]] ' if ("Depends" in attack
                                                            and attack["Depends"] == attack["Affects"]) else "",

                cypher_inject() if "Cypher" in attack else "",

                "WITH COLLECT([source, edge.Name, target, path, options, grants]) AS results, admin",
                "UNWIND results AS result",
                "WITH results, result[0] AS source,",
                "   result[1] AS edge, result[2] AS target, admin",

                # Eliminate all source nodes that incorporate other source nodes
                # producing the same edge to the same target. Nodes are validated
                # by counting the number of distinct edges produced.

                "WITH results, source,",
                "   SIZE(COLLECT(DISTINCT edge)) AS size, target, admin",
                "   WHERE size = {size}",

                "WITH results, target, ",
                "   COLLECT(DISTINCT source) AS sources, admin ",
                "WITH results, ",
                "   COLLECT(DISTINCT [target, sources]) AS pairs, admin ",

                "UNWIND pairs AS pair ",
                "UNWIND results AS result ",

                "WITH results, ",
                "result[0] AS source, result[2] AS target, ",
                "pair[0] AS t, pair[1] AS s, ",
                "TAIL(REVERSE(TAIL(NODES(result[3])))) AS intermediaries, admin ",
                "   WHERE ALL(_ IN intermediaries WHERE NOT _ IN s) ",
                "   AND target = t ",

                "WITH source, target, results, admin ",
                "UNWIND results AS result "
                "WITH source, target, result, admin "
                "   WHERE result[0] = source "
                "   AND result[2] = target "

                "WITH result[0] AS source, result[2] AS target, ",
                "   result[3] AS path, result[4] AS options, ",
                "   result[5] AS grants, admin ",

                # Attack path weight: Each outcome is representative of a distinct
                # requirement that must be satisfied for the associated path to be traversed.
                # Each path may be contingent on zero or more dependencies, represented by
                # patterns that must first be executed. This set may be empty, in which case
                # the associated weight - or the number of steps required - will be zero.

                "WITH source, target, options, grants,",
                "   [_ IN RELATIONSHIPS(path) WHERE STARTNODE(_):Pattern] AS dependencies,",
                "   LAST([_ IN RELATIONSHIPS(path)|_.Name]) AS outcome, admin",

                # [source, target, options, outcome, commands, grants, admin]

                "WITH COLLECT([source, target, options, outcome,",
                "   REDUCE(commands=[], _ IN dependencies|",
                "       CASE WHEN _ IN commands THEN commands ",
                "       ELSE commands + _.Commands END), grants]",
                "   ) AS results, admin",

                # Attack the combined minimum weight associated with each distinct source,
                # target node pair - all other results are discarded.
                # Note: this method may double count commands.

                "UNWIND results AS result",
                "WITH results, result[0] AS source, result[1] AS target,",
                "   result[3] AS outcome, MIN(SIZE(result[4])) AS weight, admin",

                "UNWIND results AS result",
                "WITH result, source, target, outcome, weight, admin",
                "   WHERE source = result[0] AND target = result[1]",
                "   AND outcome = result[3] AND weight = SIZE(result[4])",

                "WITH source, target,",
                "   REDUCE(commands=[], _ IN COLLECT(result[4])|",
                "       CASE WHEN _ IN commands THEN commands",
                "       ELSE _ + commands END) AS commands,",
                "result[2] AS options, result[5] AS grants, admin ",
            ))

        # Assert: cypher includes source, targets, options, grants, admin; where options, targets
        #         and grants comprise of (destination, commands) tuples.

        if options["AffectsGeneric"] or options["CreateAction"]:

            # Reduce result set to Generics only when a CreateAction has been specified.

            strings["affects"] += "`:`Generic"

        else:

            # A target must be either Generic or a Resource. If the target is Generic,
            # the source must be able to create it. This additional set of actions must
            # be reflected so that it can be incorporated into computed weights

            cypher += ' '.join((

                "OPTIONAL MATCH (source)-[:TRANSITIVE|ATTACK*0..{depth}]->"
                "   ()-[edge:CREATE]->(:Pattern)-->(target:Generic)",

                # Previous patterns may have already satisfied Dependency requirements. In order
                # to avoid duplicate steps, weights must be recomputed.

                "WITH source, target, options, grants,",
                "   REDUCE(commands=[], _ IN commands + COALESCE(edge.Commands,[])|",
                "       CASE WHEN _ IN commands THEN commands ",
                "       ELSE commands + _ END",
                ") AS commands, admin",

                "WHERE (NOT edge IS NULL AND target:Generic) OR target:Resource "

            ))

        # Create (source)-[:ATTACK]->(pattern:Pattern)

        cypher += ' '.join((

            "WITH DISTINCT source, target, options, grants,",
            "COALESCE(commands, []) AS commands, admin",

            # Prune targets where a transitive relationship does not exist
            # when a dependency that applies to the affected node type has
            # has been specified.

            "UNWIND options AS option "
            "WITH source, target, grants, option[0] AS option,"
            "   REDUCE(commands=[], _ IN commands + option[1]|"
            "       CASE WHEN _ IN commands THEN commands "
            "       ELSE commands + _ END"
            "   ) AS commands, admin "

            "WITH source, target, commands, grants, [[NULL, []]] AS options, admin "
            "WHERE target = option "

            if ("Depends" in attack and attack["Depends"] == attack["Affects"])
            else "ORDER BY SIZE(commands)",

            "WITH source, target, commands, options, grants, admin",
            "ORDER BY SIZE(commands)",

            "WITH DISTINCT source, options, COLLECT([target, commands]) AS grants, admin " if ("Grants" not in attack) else
            "WITH DISTINCT source, COLLECT([target, commands]) AS options, grants, admin ",

            # if any grant in admin: grants = grants ∩ admin

            "UNWIND grants AS grant ",
            "WITH source, options, grant[0] AS grant, grant[1] AS commands, ",
            "   ANY(_ IN grants WHERE _[0] IN admin) AS isadmin ",
            "WHERE NOT isadmin OR grant IN admin ",

            "WITH DISTINCT source, options, COLLECT([grant, commands]) AS grants ",

            "MERGE (source)-[edge:%s]->(pattern:Pattern:{name})" % str("CREATE" if options["CreateAction"]
                                                                       else "ATTACK"),
            "ON CREATE SET "
            "   edge.Name = \"{name}\", ",
            f"  edge.Transitive = {options['Transitive']}, " if options["CreateAction"] else "",
            "   pattern.Name = \"{name}\","
            "   pattern.Depends = \"{depends}\", ",
            "   pattern.Requires = {requires}",

            "WITH DISTINCT source, pattern, options, grants",
            "UNWIND grants AS grant",

            "WITH source, pattern, options, grant[0] AS grant, options[0][0] AS option,",
            "   REDUCE(commands=[], _ IN options[0][1] + grant[1]|",
            "       CASE WHEN _ IN commands THEN commands",
            "       ELSE commands + _ END",
            "   ) AS history",

            "WITH source, pattern, options, grant, option, ",

            cypher_resolve_commands(history=True),

            "WITH DISTINCT pattern, options, grant, option, commands ",
            "MATCH (grant) "
            "MERGE (pattern)-[edge:ATTACK{{Name:'{name}'}}]->(grant)",
            "ON CREATE SET edge.Description = {description},",
            "   edge.Created = True,",
            "   edge.Commands = commands,",
            "   edge.Weight = SIZE(commands),",
            "   edge.Option = ID(option)",

            # Create pattern options
            "WITH pattern, options "
            "UNWIND options AS option "
            "WITH pattern, option[0] AS option, option[1] AS commands "
            "MERGE (pattern)-[edge:OPTION{{Name:'Option'}}]->(option) "
            "ON CREATE SET edge.Weight = SIZE(commands), "
            "   edge.Description = {description}, "
            "   edge.Commands = commands " if (("Depends" in attack and attack["Depends"] != attack["Affects"])
                                               or "Grants" in attack) else "",

            # Used for stats
            "WITH pattern",
            "MATCH (source)-->(pattern)-[edge:ATTACK]->(grant) WHERE edge.Created",
            "OPTIONAL MATCH (pattern)-[:OPTION]->(option)",
            "REMOVE edge.Created",
            "RETURN source, edge, grant, COLLECT(DISTINCT option) AS options "
        ))

        cypher = cypher.format(**strings)

        return cypher

    def compute(self, max_iterations=5):

        converged = 0
        pruned = 0

        db = Neo4j(console=self.console)

        self.console.task("Removing all existing attacks",
                          db.run, args=["MATCH (p) WHERE p:Pattern "
                                        "   OR p.Arn = 'arn:aws:iam::{Account}:policy/Admin' "
                                        "OPTIONAL MATCH (p)-[a:ATTACK|ADMIN]->() "
                                        "DETACH DELETE p "
                                        "RETURN COUNT(a) AS deleted"
                                        ],
                          done="Removed all existing attacks"
                          )

        self.console.task("Creating pseudo Admin",
                          db.run,  args=[
                              "MERGE (admin:Admin:`AWS::Iam::Policy`{"
                              "Name: 'Effective Admin', "
                              "Description: 'Pseudo-Policy representing full and unfettered access.', "
                              "Arn: 'arn:aws:iam::{Account}:policy/Admin', "
                              'Document: \'[{"DefaultVersion": {"Version": "2012-10-17", '
                              '"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"'
                              '}]}}]\''
                              '}) '
                              "WITH admin MATCH (r:Resource) "
                              " MERGE (admin)-[access:ADMIN]->(r) "
                              " ON CREATE SET "
                              "     access.Name = 'Admin Access', "
                              "     access.Description = 'Implies all related actions and attacks' "
                          ],
                          done="Created pseudo Admin")

        attacks = [
            (list(self.definitions.keys())[i % len(self.definitions)],  # pattern name
             int(i / len(self.definitions)) + 1,  # iteration
             i % len(self.definitions) + 1  # pattern index
             ) for i in range(max_iterations * len(self.definitions))
        ]

        for (pattern, iteration, i) in self.console.tasklist(
            "Computing attack paths (this search can take a while)",
            attacks,
            done=lambda results: str("Added {count} potential attack paths"
                                     ).format(count=sum([len(s["results"]) if "results" in s else 0
                                                         for s in self.stats]) - pruned),
        ):

            if converged != 0:
                continue

            timestamp = time.time()

            self.console.info(f"Searching for attack ({i:02}/{len(self.definitions):02}): "
                              f"{pattern} (iteration: {iteration} of max: {max_iterations})")

            results = db.run(self.queries[pattern])

            for r in results:
                self.console.debug(f"Added: ({r['source']['Arn']})-->"
                                   f"({r['grant']['Arn']})")

            self.stats.append({
                "pattern": pattern,
                "iteration": iteration,
                "time_elapsed": time.time() - timestamp,
                "results": results
            })

            if (i == len(self.definitions)):  # End of iteration i

                # Check for convergence
                if (sum([len(s["results"]) for s in self.stats[-(len(self.definitions)):]]) == 0):
                    converged = iteration

                # Only retain 'cheapest' paths to Admin, using weight comprised of command length

                redundant = db.run("MATCH shortestPath((admin)-[r:ATTACK|TRANSITIVE*1..]->(:Admin)) "
                                   "    WHERE NOT (admin:Pattern OR admin:Admin) "
                                   "WITH admin MATCH path=(admin)-[r:ATTACK|TRANSITIVE*..]->(:Admin) "
                                   "WITH DISTINCT admin, path, "
                                   "    REDUCE(sum=0, _ IN [_ IN RELATIONSHIPS(path)|"
                                   "        COALESCE(_.Weight, 0)]|sum + _"
                                   "    ) AS weight "
                                   "ORDER BY admin, weight "
                                   "WITH admin, COLLECT([weight, path]) AS paths "
                                   "WITH admin, [attack IN NODES(paths[0][1]) WHERE attack:Pattern] AS cheapest "
                                   "MATCH path=(admin)-[:ATTACK]->(pattern:Pattern) "
                                   "    WHERE NOT pattern IN cheapest "
                                   "WITH pattern MATCH (source)-[attack:ATTACK]->(pattern) "
                                   "MERGE (source)-[redundant:REDUNDANT]->(pattern) "
                                   "    ON CREATE SET redundant = attack "
                                   "DELETE attack "
                                   "WITH pattern MATCH pruned=()-[:REDUNDANT]->(pattern)-[:ATTACK]->() "
                                   "RETURN COUNT(pruned) AS pruned"
                                   )[0]["pruned"]

                if redundant > 0:
                    self.console.debug(f"{redundant} redundant admin paths "
                                       "have been marked for deletion")
                pruned += redundant

                # Achieved convergence: no new attacks were discovered during the iteration
                if converged != 0 or iteration == max_iterations:

                    if converged == 0:

                        self.console.debug("Reached maximum number of iterations "
                                           f"({max_iterations}) - Tidying up")
                    else:
                        self.console.debug("Search converged on iteration: "
                                           f"{iteration} of max: {max_iterations} - Tidying up")

                    # Update attack descriptions
                    db.run("MATCH (:Pattern)-[attack:ATTACK|OPTION|CREATE]->() "
                           "WHERE SIZE(attack.Commands) > 0 "
                           "WITH COLLECT(DISTINCT attack) AS attacks "
                           "UNWIND attacks AS attack "

                           # Construct a lookup table comprising of command, description pairs.
                           "WITH attacks, attack, "
                           "   SIZE(attack.Commands) - SIZE(attack.Description) AS offset "
                           "WITH attacks, offset, attack, "
                           "   [i IN RANGE(0, SIZE(attack.Commands) -1)|[attack.Commands[i], "
                           "       CASE WHEN i - offset < 0 THEN NULL "
                           "       ELSE attack.Description[i - offset] END]] "
                           "   AS lookups "

                           # Remove NULL value command, description pairs
                           "WITH attacks, lookups "
                           "UNWIND lookups AS lookup "
                           "WITH DISTINCT attacks, lookup "
                           "   WHERE lookup[1] IS NOT NULL "
                           "WITH COLLECT(lookup) AS lookups, attacks "
                           "UNWIND attacks AS attack "

                           # Map attack commands to descriptions
                           "WITH attack, lookups, ["
                           "   description IN [command IN attack.Commands|"
                           "       [lookup in lookups WHERE lookup[0] = command][0][1]] "
                           "   WHERE description IS NOT NULL"
                           "] AS descriptions "

                           "SET attack.Descriptions = descriptions "
                           "REMOVE attack.Description"
                           )

                    # Remove redundant attack paths
                    db.run("MATCH ()-[:REDUNDANT]->(pattern:Pattern)-[redundant:ATTACK]->() "
                           "DETACH DELETE pattern "
                           "RETURN COUNT(DISTINCT redundant) AS pruned"
                           )

                    # Remove attacks affecting generic resources
                    pruned += db.run(
                        "MATCH (:Pattern)-[attack:ATTACK]->(:Generic) "
                        "DELETE attack "
                        "WITH COUNT(attack) AS pruned "
                        "OPTIONAL MATCH (p:Pattern) WHERE NOT EXISTS((p)-[:ATTACK|CREATE]->()) "
                        "DETACH DELETE p "
                        "RETURN pruned"
                    )[0]["pruned"]

        db.close()
