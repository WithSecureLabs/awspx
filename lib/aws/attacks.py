
import copy
import json
import re
import time

from lib.graph.db import Neo4j


definitions = {

    "CreatePolicyVersion": {

        "Description": "Overwrite the default version of the "
        "target managed policy:",

        "Commands": [
            "aws create-policy-version "
            "--policy-arn ${AWS::Iam::Policy}.Arn "
            "--set-as-default "
            "--policy-document file://<(cat <<EOF\n"
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

        "Description": "Associate the specified EC2 instance with "
        "the target instance profile: ",

        "Commands": [
            "aws ec2 associate-iam-instance-profile "
            "--iam-instance-profile Name=${AWS::Iam::InstanceProfile} "
            "--instance-id ${AWS::Ec2::Instance}"
        ],

        "Attack": {

            "Depends": "AWS::Ec2::Instance",

            "Requires": [
                "ec2:AssociateIamInstanceProfile"
            ],

            "Affects": "AWS::Ec2::Instance",

            "Grants": "AWS::Iam::InstanceProfile",

            "Cypher": [
                "(${AWS::Ec2::Instance}) WHERE NOT EXISTS((${AWS::Iam::InstanceProfile})-[:TRANSITIVE]->(:`AWS::Iam::Role`)) "
                "OR EXISTS((${AWS::Iam::InstanceProfile})-[:TRANSITIVE]->(:`AWS::Iam::Role`)<-[:ACTION{Name:'iam:PassRole', Effect:'Allow'}]-(${}))"
            ]

        }
    },

    "AssumeRole": {

        "Description": "Retrieve a set of temporary security credentials "
        "from assuming the target role:",

        "Commands": [
            "aws sts assume-role "
            "--role-arn ${AWS::Iam::Role}.Arn "
            "--role-session-name AssumeRole"
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

        "Description": "Add the target role to "
        "the specified instance profile:",

        "Commands": [
            "aws iam add-role-to-instance-profile"
            "--instance-profile-name ${AWS::Iam::InstanceProfile} "
            "--role-name ${AWS::Iam::Role}"],

        "Attack": {

            "Depends": "AWS::Iam::InstanceProfile",

            "Requires": [
                "iam:AddRoleToInstanceProfile"
            ],

            "Affects": "AWS::Iam::InstanceProfile",

            "Grants": "AWS::Iam::Role",

            "Cypher": [
                "(${AWS::Iam::Role})-[:TRUSTS]->({Name:'ec2.amazonaws.com'}) "
                "WHERE (${})-[:TRANSITIVE|ATTACK*0..]->()-[:ACTION{Effect:'Allow', Name:'iam:RemoveRoleFromInstanceProfile'}]->(${AWS::Iam::InstanceProfile}) "
                "OR (${})-[:TRANSITIVE|ATTACK*0..]->()-[:ACTION{Effect:'Allow', Name:'iam:DeleteInstanceProfile'}]->(${AWS::Iam::InstanceProfile}) "
                "OR NOT EXISTS((${AWS::Iam::InstanceProfile})-[:TRANSITIVE]->(${AWS::Iam::Role})) "
            ]
        }
    },

    "AddUserToGroup": {

        "Description": "Add the specified user to the target group:",

        "Commands": [
            "aws iam add-user-to-group "
            "--user-name ${AWS::Iam::User} "
            "--group-name ${AWS::Iam::Group}"
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

        "Description": "Attach the target managed "
        "policy to the specified group:",

        "Commands": [
            "aws iam attach-group-policy "
            "--group-name ${AWS::Iam::Group} "
            "--policy-arn ${AWS::Iam::Policy}.Arn",
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

        "Description": "Attach the target managed "
        "policy to the specified role:",

        "Commands": [
            "aws iam attach-role-policy "
            "--role-name ${AWS::Iam::Role} "
            "--policy-arn ${AWS::Iam::Policy}.Arn"
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

        "Description": "Attach the target managed "
        "policy to the specified user.",

        "Commands": [
            "aws iam attach-user-policy "
            "--user-name ${AWS::Iam::User} "
            "--policy-arn ${AWS::Iam::Policy}.Arn",
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

        "Options": ["CreateAction"],

        "Commands": [
            "aws iam create-group --group-name ${AWS::Iam::Group}",

            "aws iam add-user-to-group "
            "--user-name ${AWS::Iam::User} "
            "--group-name ${AWS::Iam::Group}"
        ],

        "Attack": {

            "Depends": "AWS::Iam::User",

            "Requires": [
                "iam:CreateGroup",
                "iam:AddUserToGroup",
            ],

            "Affects": "AWS::Iam::Group"

        },
    },

    "CreateInstance": {

        "Description": "Launch a new EC2 instance:",

        "Options": ["CreateAction"],

        "Commands": [
            "aws ec2 run-instances "
            "--count 1 "
            "--instance-type t2.micro"
            "--image-id $AmiId",
        ],

        "Attack": {

            "Requires": [
                "ec2:RunInstances"
            ],

            "Affects": "AWS::Ec2::Instance",

        }
    },

    "CreateInstanceProfile": {

        "Description": "Create a new instance profile",

        "Options": ["CreateAction"],

        "Commands": [
            "aws iam create-instance-profile "
            "--instance-profile-name ${AWS::Iam::InstanceProfile}"
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

        "Options": ["CreateAction"],

        "Commands": [
            "aws iam create-policy "
            "--policy-name ${AWS::Iam::Policy} "
            "--policy-document file://<(cat <<EOF\n"
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

        },
    },

    "CreateRole": {

        "Description": "Create a new role to assume:",

        "Options": ["CreateAction"],

        "Commands": [
            "aws iam create-role --role-name ${AWS::Iam::Role} "
            "--assume-role-policy-document file://<(cat <<EOF\n"
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
            ")"
        ],

        # TODO: If this attack incorporates an instance profile then the Principal entry
        # in Commands should be Service: ec2.amazonaws.com.
        "Attack": {

            "Requires": [
                "iam:CreateRole",
            ],

            "Affects": "AWS::Iam::Role",

        },

        "Grants": "AssumeRole"
    },

    "CreateUserLoginProfile": {

        "Description": "Create a new user:",

        "Options": ["CreateAction"],

        "Commands": [
            "aws iam create-user --user-name ${AWS::Iam::User}",
            "aws iam create-login-profile --user-name ${AWS::Iam::User} "
            "--password $Password"
        ],

        "Attack": {

            "Requires": [
                "iam:CreateUser",
                "iam:CreateLoginProfile"
            ],

            "Affects": "AWS::Iam::User",

        }
    },

    "PutGroupPolicy": {

        "Description": "Add a new administrative inline policy document to the target group:",

        "Commands": [
            "aws iam put-group-policy --group-name ${AWS::Iam::Group} "
            "--policy-name Admin "
            "--policy-document file://<(cat <<EOF\n"
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
            "aws iam put-role-policy --role-name ${AWS::Iam::Role} "
            "--policy-name Admin "
            "--policy-document file://<(cat <<EOF\n"
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
            "aws iam put-user-policy --user-name ${AWS::Iam::User} "
            "--policy-name Admin "
            "--policy-document file://<(cat <<EOF\n"
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

        "Description": "Update the assume-role policy document of "
        "the target role and assume it thereafter:",

        "Commands": [
            "aws iam update-assume-role-policy --role-name ${AWS::Iam::Role} "
            "--policy-document file://<(cat <<EOF\n"
            "{\n"
            "  \"Version\": \"2012-10-17\",\n"
            "  \"Statement\": [\n"
            "    {\n"
            "      \"Effect\": \"Allow\",\n"
            "      \"Action\": \"sts:AssumeRole\",\n"
            "      \"Principal\": {\n"
            "        \"AWS\": [\n"
            "          \"${}.Arn\"\n"
            "        ]\n"
            "      }\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "EOF\n"
            ")",

            "aws sts assume-role "
            "--role-arn ${AWS::Iam::Role}.Arn "
            "--role-session-name AssumeRole"
        ],

        "Attack": {

            "Requires": [
                "iam:UpdateAssumeRolePolicy"
            ],

            "Affects": "AWS::Iam::Role"

        }
    },

    "UpdateUserLoginProfile": {

        "Description": "Reset the target user's console password and login as them:",

        "Commands": [
            "aws iam update-login-profile "
            "--user-name ${AWS::Iam::User} "
            "--password $Password "
        ],

        "Attack": {

            "Requires": [
                "iam:UpdateLoginProfile"
            ],

            "Affects": "AWS::Iam::User"

        }
    },

    "SetUserLoginProfile": {

        "Description": "Set a console password for the target user and login as them, nothing has been set before:",

        "Commands": [
            "aws iam create-login-profile "
            "--user-name ${AWS::Iam::User} "
            "--password $Password "
        ],

        "Attack": {

            "Requires": [
                "iam:CreateLoginProfile"
            ],

            "Affects": "AWS::Iam::User",

            "Cypher": [
                "${AWS::Iam::User}.LoginProfile IS NULL"
            ]
        }
    },

    "CreateUserAccessKey": {

        "Description": "Create an access key for the target user and authenticate as them using the API:",

        "Commands": [
            "aws iam create-access-key "
            "--user-name ${AWS::Iam::User} "
        ],

        "Attack": {

            "Requires": [
                "iam:CreateAccessKey"
            ],

            "Affects": "AWS::Iam::User",

            "Cypher": [
                "(COALESCE(SIZE(SPLIT("
                "${AWS::Iam::User}.AccessKeys,"
                "'Status')), 1) - 1) < 2",
            ]

        }
    },

    "ReplaceUserAccessKey": {

        "Description": "Create, or replace, an access key for the target user and authenticate as them using the API:",

        "Commands": [
            "aws iam delete-access-key "
            "--user-name ${AWS::Iam::User} "
            "--access-key-id $AccessKeyId",
            "aws iam create-access-key "
            "--user-name ${AWS::Iam::User} "
        ],

        "Attack": {

            "Requires": [
                "iam:DeleteAccessKey",
                "iam:CreateAccessKey"
            ],

            "Affects": "AWS::Iam::User",

            "Cypher": [
                "(SIZE(SPLIT("
                "${AWS::Iam::User}.AccessKeys,"
                "'Status')) - 1) > 0",
            ]

        }
    },

}


class Attacks:

    definitions = definitions
    stats = []

    def __init__(self, skip_attacks=[], only_attacks=[], skip_conditional_actions=True, console=None):

        if console is None:
            from lib.util.console import console
        self.console = console

        self.ignore_actions_with_conditions = skip_conditional_actions
        self.definitions = {k: v for k, v in self.definitions.items()
                            if k not in skip_attacks
                            and (only_attacks == [] or k in only_attacks)}

    def _pattern_cypher(
            self,
            name,
            definition,
            max_search_depth=""):

        definition = copy.deepcopy(definition)
        attack = definition["Attack"]

        CYPHER = ""
        VARs = {
            "name": name,
            "description": definition["Description"],
            "commands": definition["Commands"],
            "depends": attack["Depends"] if "Depends" in attack else "",
            "affects": attack["Affects"],
            "requires": attack["Requires"],
            "grants": attack["Grants"] if "Grants" in attack else "",
            "depth": max_search_depth,
            "steps": len(definition["Commands"]),
            "size": len(attack["Requires"]),
        }

        OPTs = {
            "CreateAction": True if "Options" in definition and "CreateAction" in definition["Options"] else False,
            "Admin": True if "Grants" in attack and attack["Grants"] == "Admin" else False
        }

        def cypher_resolve_commands(history=False):

            # A nested REPLACE operation must occur for every placeholder in the
            # format string, each of which has to be resolved. Resolution occurs
            # by performing a type comparison against fields in the pattern's
            # definition.

            _CYPHER_ = "_"

            for (placeholder, attr) in sorted(
                re.findall(r"\$\{(AWS\:\:[A-Za-z0-9]+\:\:[A-Za-z0-9]+)?\}(\.[A-Za-z]+)?",
                           ';'.join(VARs["commands"])),
                key=lambda x: len(x[0]+x[1]),
                    reverse=True):

                substitute = None

                if placeholder == attack["Affects"]:
                    substitute = "grant" if "Grants" not in attack else "option"
                elif "Depends" in attack \
                        and placeholder == attack["Depends"]:
                    substitute = "option"
                elif "Grants" in attack \
                        and placeholder == attack["Grants"]:
                    substitute = "grant"
                elif placeholder == '':
                    substitute = "source"
                else:
                    self.console.debug(f"Unknown placeholder: '{placeholder}'")
                    continue

                placeholder = f"${{{placeholder}}}"

                if len(attr) == 0:
                    substitute += ".Name"
                else:
                    substitute += attr
                    placeholder += attr

                _CYPHER_ = "REPLACE(%s, \"%s\", %s)" \
                    % (_CYPHER_, placeholder, substitute)

            _CYPHER_ = ("EXTRACT(_ IN %s|%s)" % (VARs["commands"], _CYPHER_)
                        ).replace('{', '{{').replace('}', '}}')

            if history:

                _CYPHER_ = (
                    "REDUCE(commands=[], _ IN history + %s|"
                    "CASE WHEN _ IN commands THEN commands "
                    "ELSE commands + _ END) "
                    "AS commands") % (_CYPHER_)

            else:
                _CYPHER_ += " AS commands"

            return _CYPHER_

        def resolve_placeholder(placeholder):

            if "${}" == placeholder:
                return "source"

            elif "${%s}" % attack["Affects"] == placeholder:
                return "target"

            elif "Depends" in attack  \
                    and "${%s}" % attack["Depends"] == placeholder:
                return "option"

            elif "Grants" in attack  \
                    and "${%s}" % attack["Grants"] == placeholder:
                return "grant"

            else:
                r = re.compile(
                    "\$\{(AWS\:\:[A-Za-z0-9:]+)\}").match(placeholder)

                if r.group(1) is not None:
                    return "%s:`%s`" % (r.group(1).replace(':', '').lower(), r.group(1))

                # else:
                #     notice("subject %s malformed" % placeholder, True)

        def process_cypher():

            WITH = ["source", "edge", "options",
                    "target", "path", "grants", "admin"]
            CONSTRAINTS = attack["Cypher"]
            UNWIND = []

            placeholders = {
                k: resolve_placeholder(k) for k in set(
                    [r for (r, _) in re.findall(
                        r"(\$\{(AWS\:\:[A-Za-z0-9]+\:\:[A-Za-z0-9]+)?\})",
                        ' '.join(attack["Cypher"]))])
            }

            for i in range(len(CONSTRAINTS)):

                for k, v in placeholders.items():
                    if v not in UNWIND \
                            and (v == "option" or v == "grant"):
                        UNWIND.append(v)
                    CONSTRAINTS[i] = CONSTRAINTS[i].replace(k, v)

                CONSTRAINTS[i] = CONSTRAINTS[i].replace(
                    "{", "{{").replace(
                    "}", "}}")

            if len(UNWIND) > 0:

                CONSTRAINTS = " ".join((
                    "WITH %s" % ", ".join(WITH),
                    "%s" % " ".join(["UNWIND %s AS %s" % (i, i[:-1])
                                     for i in WITH
                                     if i[:-1] in UNWIND]),
                    "WITH %s" % ", ".join(
                        [i if i[:-1] not in UNWIND
                            else "{i}[0] AS {i}, {i}[1] AS {i}_commands".format(i=i[:-1])
                            for i in WITH]),
                    "MATCH %s" % ', '.join(CONSTRAINTS),
                    "WITH %s" % ", ".join(
                        [i if i[:-1] not in UNWIND
                            else "COLLECT([{i},{i}_commands]) AS {j}".format(i=i[:-1], j=i)
                            for i in WITH])
                ))

            else:
                CONSTRAINTS = "AND %s" % "AND ".join(CONSTRAINTS)

            return CONSTRAINTS

        # If a node, or edge, is identified to grant Admin, it is excluded from
        # search. This is because all patterns incorporating Admin are implied
        # - searching further would be redundant.

        CYPHER += (
            "OPTIONAL MATCH (admin)-[:ATTACK|TRANSITIVE*0..]->(:Admin), "
            "(default:Admin{{Arn:'arn:aws:iam::${{Account}}:policy/Admin'}}) "
            "WHERE NOT (admin:Pattern OR admin:Admin) "
            "WITH COLLECT(DISTINCT COALESCE(admin, default)) AS admin, "
            "[[NULL, []]] AS options, [NULL, []] AS grants "
        )

        # Patterns including a "Depends" value require an additional argument, which must
        # be reachable. This amounts to determining whether any nodes of that type can
        # be reached (transitively, or through performing one or more attacks).
        # Consequently, it must incorporate a weight that is computed once all required
        # commands have been consilidated. Dependencies need to be determined first in
        # order to avoid erroneous exclusion when we perfrom deduplication later.

        if "Depends" in attack:

            VARs["option_type"] = attack["Depends"]

            CYPHER += (
                "MATCH path=(source)-"
                "[:TRANSITIVE|ATTACK*0..{depth}]->()-[:CREATE*0..1]->(option:`{option_type}`) "
                "WHERE NOT source IN admin AND NOT option IN NODES(path)[1..-1] "
                "AND (source:Resource OR source:External) AND (option:Resource OR option:Generic) "

                "WITH DISTINCT source, option, admin, "
                "FILTER(_ IN RELS(path) WHERE STARTNODE(_):Pattern) AS dependencies "

                "WITH admin, COLLECT([source, option, REDUCE("
                "commands=[], _ IN dependencies|"
                "CASE WHEN _ IN commands THEN commands "
                "ELSE commands + _.Commands END)]"
                ") AS results "

                "UNWIND results AS result "

                "WITH admin, results, result[0] AS source, result[1] AS option, "
                "MIN(SIZE(result[2])) AS weight "

                "UNWIND results AS result "
                "WITH admin, result, source, option, weight, result[2] AS commands "
                "WHERE source = result[0] AND option = result[1] "
                "AND weight = SIZE(result[2]) "

                "WITH admin, source, option, commands, weight ORDER BY weight "
                "WITH admin, source, COLLECT([option, commands]) AS options, [NULL, []] AS grants "
            )

        if "Grants" in attack:

            CYPHER += ''.join((

                "OPTIONAL MATCH (grant:`{grants}`) WHERE NOT grant:Generic ",
                str("AND grant:Resource " if attack["Grants"] != "Admin"
                    else ""),
                "OPTIONAL MATCH creation=shortestPath((source)-"
                "[:TRANSITIVE|ATTACK|CREATE*..{depth}]->(generic:Generic:`{grants}`)) ",
                "WHERE source <> generic ",

                "WITH DISTINCT source, options, admin, ",
                "grant, generic, REDUCE(commands=[], _ IN EXTRACT(",
                "_ IN FILTER(_ IN RELS(creation) ",
                "WHERE STARTNODE(_):Pattern)|_.Commands)|",
                "CASE WHEN _ IN commands THEN commands ",
                "ELSE commands + _ END",
                ") AS commands ",

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

        if VARs["size"] == 1 and "Depends" not in attack and "Cypher" not in attack:

            # If only one relationship is required, and there are no dependencies,
            # only direct relationships need to be identified, weight computation
            # and pruning requirements can be safely ommitted.

            CYPHER += ' '.join((
                "MATCH path=(source)-[edge:ACTION{{Name:'{requires[0]}', Effect: 'Allow'}}]"
                "->(target:`{affects}`) ",

                "WHERE NOT source:Pattern ",
                "AND ALL(_ IN REVERSE(TAIL(REVERSE(NODES(path)))) WHERE NOT _ IN admin) ",
                "AND edge.Condition = '[]' " if self.ignore_actions_with_conditions else "",

                # TODO: This is just a quick fix for target types that are dependant on being reachable transitively.
                # As is, it will still produce false positives - just less than before.

                'AND target IN [_ IN options|_[0]] ' if "Depends" in attack and attack["Depends"] == attack["Affects"] else "",

                "%s" % process_cypher() if "Cypher" in attack else "",

                "WITH source, target, [] AS commands, options, grants, admin ",
            ))
        else:

            # Otherwise, the attack may incorporate indirect relationships (a dependency or
            # or a combination of one or more relationships.

            CYPHER += ' '.join((

                "MATCH path=(source)-"
                "[:TRANSITIVE|ATTACK*0..{depth}]->()"
                "-[edge:ACTION]->(target:`{affects}`)",

                "WHERE NOT source:Pattern",
                "AND ALL(_ IN REVERSE(TAIL(REVERSE(NODES(path)))) WHERE NOT _ IN admin)",
                "AND edge.Name IN {requires} AND edge.Effect = 'Allow' ",
                "AND edge.Condition = '[]' " if self.ignore_actions_with_conditions else "",
                'AND target IN [_ IN options|_[0]] ' if "Depends" in attack and attack["Depends"] == attack["Affects"] else "",
                "%s" % process_cypher() if "Cypher" in attack else "",

                "WITH COLLECT([source, edge.Name, target, path, options, grants]) AS results, admin",

                "UNWIND results AS result",
                "WITH results, result[0] AS source,",
                "result[1] AS edge, result[2] AS target, admin",

                # Eliminate all source nodes that incorporate other source nodes
                # producing the same edge to the same target. Nodes are validated
                # by counting the number of distinct edges produced.

                "WITH results, source,",
                "SIZE(COLLECT(DISTINCT edge)) AS size, target, admin",
                "WHERE size = {size}",

                "WITH results, target, ",
                "COLLECT(DISTINCT source) AS sources, admin ",
                "WITH results, ",
                "COLLECT(DISTINCT [target, sources]) AS pairs, admin ",

                "UNWIND pairs AS pair ",
                "UNWIND results AS result ",

                "WITH results, ",
                "result[0] AS source, result[2] AS target, ",
                "pair[0] AS t, pair[1] AS s, ",
                "TAIL(REVERSE(TAIL(NODES(result[3])))) AS intermediaries, admin ",
                "WHERE ALL(_ IN intermediaries WHERE NOT _ IN s) ",
                "AND target = t ",

                "WITH source, target, results, admin ",
                "UNWIND results AS result "
                "WITH source, target, result, admin "
                "WHERE result[0] = source "
                "AND result[2] = target "

                "WITH result[0] AS source, result[2] AS target, ",
                "result[3] AS path, result[4] AS options, ",
                "result[5] AS grants, admin ",

                # Attack path weight: Each outcome is representative of a distinct
                # requirement that must be satisfied for the associated path to be traversed.
                # Each path may be contingent on zero or more dependencies, represented by
                # patterns that must first be executed. This set may be empty, in which case
                # the associated weight - or the number of steps required - will be zero.

                "WITH source, target, options, grants,",
                "FILTER(_ IN RELS(path) WHERE STARTNODE(_):Pattern) AS dependencies,",
                "LAST(EXTRACT(_ IN RELS(path)|_.Name)) AS outcome, admin",

                # [source, target, options, outcome, commands, grants, admin]

                "WITH COLLECT([source, target, options, outcome,",
                "REDUCE(commands=[], _ IN dependencies|",
                "CASE WHEN _ IN commands THEN commands ",
                "ELSE commands + _.Commands END), grants]",
                ") AS results, admin",

                # Attack the combined minimum weight associated with each distinct source,
                # target node pair - all other results are discarded.
                # Note: this method may double count commands.

                "UNWIND results AS result",
                "WITH results, result[0] AS source, result[1] AS target,",
                "result[3] AS outcome, MIN(SIZE(result[4])) AS weight, admin",

                "UNWIND results AS result",
                "WITH result, source, target, outcome, weight, admin",
                "WHERE source = result[0] AND target = result[1]",
                "AND outcome = result[3] AND weight = SIZE(result[4])",

                "WITH source, target,",
                "REDUCE(commands=[], _ IN COLLECT(result[4])|",
                "CASE WHEN _ IN commands THEN commands",
                "ELSE _ + commands END) AS commands,",
                "result[2] AS options, result[5] AS grants, admin ",
            ))

        # Assert: CYPHER includes source, targets, options, grants, admin; where options, targets
        #         and grants comprise of (destination, commands) tuples.

        if OPTs["CreateAction"]:

            # Reduce result set to Generics only when a CreateAction has been specified.

            VARs["affects"] += "`:`Generic"

        else:

            # A target must be either Generic or a Resource. If the target is Generic,
            # the source must be able to create it. This additional set of actions must
            # be reflected so that it can be incorporated into computed weights

            CYPHER += ' '.join((

                "OPTIONAL MATCH (source)-[:TRANSITIVE|ATTACK*0..{depth}]->()"
                "-->(:Pattern)-[edge:CREATE]->(target:Generic)",

                # Previous patterns may have already satisfied Dependency requirements. In order
                # to avoid duplicate steps, weights must be recomputed.

                "WITH source, target, options, grants,",
                "REDUCE(commands=[], _ IN commands + COALESCE(edge.Commands,[])|",
                "CASE WHEN _ IN commands THEN commands ",
                "ELSE commands + _ END",
                ") AS commands, admin",

                "WHERE (NOT edge IS NULL AND target:Generic) OR target:Resource "

            ))

        # Create (source)-[:ATTACK]->(pattern:Pattern)

        CYPHER += ' '.join((

            "WITH DISTINCT source, target, options, grants,",
            "COALESCE(commands, []) AS commands, admin",

            # Prune targets where a transitive relationship does not exist
            # when a dependency that applies to the affected node type has
            # has been specified.

            "UNWIND options AS option "
            "WITH source, target, grants, "
            "option[0] AS option,"
            "REDUCE(commands=[], _ IN commands + option[1]|"
            "CASE WHEN _ IN commands THEN commands "
            "ELSE commands + _ END"
            ") AS commands, admin "

            "WITH source, target, commands, grants, [[NULL, []]] AS options, admin "
            "WHERE target = option "

            if "Depends" in attack \
            and attack["Depends"] == attack["Affects"]
            else "ORDER BY SIZE(commands)",

            "WITH source, target, commands, options, grants, admin",
            "ORDER BY SIZE(commands)",

            "WITH DISTINCT source, options, COLLECT([target, commands]) AS grants, admin " \
            if "Grants" not in attack else \
            "WITH DISTINCT source, COLLECT([target, commands]) AS options, grants, admin ",

            # if any grant in admin: grants = grants ∩ admin

            "UNWIND grants AS grant ",
            "WITH source, options, grant[0] AS grant, grant[1] AS commands, ",
            "ANY(_ IN EXTRACT(_ IN grants| _[0] IN admin) WHERE _) AS isadmin ",
            "WHERE NOT isadmin OR grant IN admin ",

            "WITH DISTINCT source, options, COLLECT([grant, commands]) AS grants ",

            "MERGE (source)-[:ATTACK{{Name:'{name}'}}]-> "
            "(pattern:Pattern:{name}{{Name:'{name}'}})",
            "ON CREATE SET ",
            "pattern.Requires = {requires},",
            "pattern.Depends = \"{depends}\"",

            "WITH DISTINCT source, pattern, options, grants",
            "UNWIND grants AS grant",

            "WITH source, pattern, options,",
            "grant[0] AS grant, options[0][0] AS option,",
            "REDUCE(commands=[], _ IN options[0][1] + grant[1]|",
            "CASE WHEN _ IN commands THEN commands",
            "ELSE commands + _ END",
            ") AS history",

            "WITH source, pattern, options, grant, option, ",
            "%s" % cypher_resolve_commands(True),

            "WITH DISTINCT pattern, options, grant, option, commands ",
            "MATCH (grant) "
            "MERGE (pattern)-[edge:%s{{Name:'{name}'}}]->(grant)" \
            % ("CREATE" if OPTs["CreateAction"] \
                else "ATTACK"),
            "ON CREATE SET ",
            "edge.Description = \"{description}\",",
            "edge.Commands = commands,",
            "edge.Weight = SIZE(commands),",
            "edge.Option = ID(option)",
            ", edge.Admin = True " if OPTs["Admin"] else ""

            # Create pattern options

            "WITH pattern, options "
            "UNWIND options AS option "
            "WITH pattern, option[0] AS option, option[1] AS commands "
            "MERGE (pattern)-[edge:OPTION{{Name:'Option'}}]->(option) "
            "ON CREATE SET "
            "edge.Weight = SIZE(commands), "
            "edge.Description = \"{description}\", "
            "edge.Commands = commands " \
            if ("Depends" in attack and attack["Depends"] != attack["Affects"]) \
            or "Grants" in attack \
            else ""
        ))

        CYPHER = CYPHER.format(**VARs)

        return CYPHER

    def compute(self, max_iterations=5, max_search_depth=""):

        converged = False
        db = Neo4j(console=self.console)

        self.console.task("Removing all existing attack patterns",
                          db.run,  args=["MATCH (p:Pattern) DETACH DELETE p"],
                          done="Removed all existing attack patterns")

        self.console.task("Creating pseudo Admin",
                          db.run,  args=[
                              "MERGE (admin:Admin:`AWS::Iam::Policy`{"
                              "Name: 'Effective Admin', "
                              "Description: 'Pseudo-Policy representing full and unfettered access.', "
                              "Arn: 'arn:aws:iam::${Account}:policy/Admin', "
                              'Document: \'[{"DefaultVersion": {"Version": "2012-10-17", '
                              '"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"'
                              '}]}}]\''
                              '}) '
                          ],
                          done="Created pseudo Admin")

        for i in self.console.tasklist(
            "Adding attack paths (this search can take a while)",
            range(max_iterations * len(self.definitions)),
            done="Added attack paths"
        ):
            if converged:
                continue

            # First iteration
            elif (i % len(self.definitions) == 0):
                self.console.info("Temporarily adding Admin label "
                                  "to Generic Policy")
                db.run("MATCH (gp:`AWS::Iam::Policy`:Generic) SET gp:Admin")

            # Last iteration, check for convergence
            elif ((i + 1) % len(self.definitions) == 0):

                self.console.info("Removing Admin label from Generic Policy")
                db.run("MATCH (admin:`AWS::Iam::Policy`:Generic) "
                       "REMOVE admin:Admin")

                self.console.info("Pruning attack paths")

                # Only keep the 'cheapest' paths to admin, favouring transitive
                # relationships over attacks
                db.run("MATCH shortestPath((admin)-[:ATTACK|TRANSITIVE*1..]->(:Admin)) "
                       "WHERE NOT (admin:Pattern OR admin:Admin) "
                       "WITH admin MATCH path=(admin)-[:ATTACK|:TRANSITIVE*..]->(:Admin) "
                       "WITH DISTINCT admin, path, "
                       "REDUCE(sum=0, _ IN EXTRACT(_ IN RELS(path)|"
                       "COALESCE(_.Weight, 0))|sum + _) AS weight "
                       "ORDER BY admin, weight "
                       "WITH admin, COLLECT([weight, path]) AS paths "
                       "WITH admin, FILTER(attack IN NODES(paths[0][1]) "
                       "WHERE attack:Pattern) AS cheapest "
                       "MATCH path=(admin)-[:ATTACK]->(pattern:Pattern) "
                       "WHERE NOT pattern IN cheapest "
                       "WITH pattern MATCH (source)-[attack:ATTACK]->(pattern) "
                       "MERGE (source)-[_attack_:_ATTACK_]->(pattern) "
                       "ON CREATE SET _attack_ = attack "
                       "DELETE attack"
                       )

                db.run("MATCH (admin)-[:ATTACK*..2]->(:Admin) "
                       "WITH COLLECT(DISTINCT admin) AS admins "
                       "WITH admins UNWIND admins AS admin "
                       "MATCH (source)-[:TRANSITIVE*1..]->(target) "
                       "WHERE target IN admins "
                       "WITH DISTINCT source "
                       "MATCH (source)-[attack:ATTACK]->(pattern:Pattern) "
                       "MERGE (source)-[_attack_:_ATTACK_]->(pattern) "
                       "ON CREATE SET _attack_ = attack "
                       "DELETE attack "
                       )

                if sum([s["nodes_created"] + s["relationships_created"]
                        for s in self.stats[-(len(self.definitions)):]]) == 0:

                    converged = True
                    self.console.info("Search converged on iteration: "
                                      f"{iteration} of max: {max_iterations} - "
                                      "Tidying up")

                    # Update attack descriptions
                    db.run("MATCH (:Pattern)-[attack:ATTACK|OPTION|CREATE]->() "
                           "WHERE LENGTH(attack.Commands) > 0 "
                           "WITH COLLECT(DISTINCT attack) AS attacks "
                           "UNWIND attacks AS attack "
                           "WITH attacks, COLLECT(DISTINCT ["
                           "    attack.Commands[LENGTH(attack.Commands) - 1], "
                           "    attack.Description]) as commands "
                           "UNWIND attacks AS attack "
                           "WITH attack, commands WHERE TYPE(attack) = 'ATTACK' "
                           "WITH attack, EXTRACT(command IN attack.Commands|"
                           "    COALESCE([description IN commands "
                           "        WHERE command = description[0]][0][1], "
                           "        attack.Description)) AS descriptions "
                           "WITH attack, descriptions "
                           "SET attack.Descriptions = descriptions "
                           "REMOVE attack.Description"
                           )

                    # Remove redundant attack paths
                    db.run("MATCH ()-[:_ATTACK_]->(pattern:Pattern) "
                           "DETACH DELETE pattern"
                           )
                    # Remove attacks affecting generic resources
                    db.run("OPTIONAL MATCH ()-[:ATTACK]->(:Pattern)-[attack:ATTACK]->(:Generic) "
                           "DELETE attack"
                           )

                    continue

            pattern = list(self.definitions.keys())[i % len(self.definitions)]
            iteration = int(i / len(self.definitions)) + 1
            definition = self.definitions[pattern]
            timestamp = time.time()

            self.console.info(f"Searching for attack: {pattern} "
                              f"(iteration: {iteration} of max: {max_iterations})")

            cypher = self._pattern_cypher(pattern, definition,
                                          max_search_depth)

            summary = db.run(cypher)._summary

            self.stats.append({
                "pattern": pattern,
                "iteration": iteration,
                "nodes_created": 0,
                "relationships_created": 0,
                "properties_set": 0,
                "labels_added": 0,
                "time_elapsed": time.time() - timestamp,
                ** summary.counters.__dict__
            })

        db.close()

        discovered = sum([s["nodes_created"] if "nodes_created" in s
                          else 0 for s in self.stats])

        self.console.notice(f"{discovered} potential attack paths "
                            "were added to the database")
