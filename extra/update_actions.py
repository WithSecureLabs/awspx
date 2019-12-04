#!/usr/bin/python3


import requests
import pandas
import json
import sys
import re

# Because the linter keeps fu#*ing up these imports
if True:
    sys.path.append('..')
    from bs4 import BeautifulSoup
    from lib.aws.resources import RESOURCES


Services = {

    # Implemented

    'Iam': {
        "URL": 'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_identityandaccessmanagement.html'
    },

    "Sts": {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awssecuritytokenservice.html",
    },

    'Ec2': {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonec2.html"
    },

    "S3": {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html",
    },

    "Lambda": {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awslambda.html"
    },

    # Partially implemented

    "CloudFormation": {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awscloudformation.html"
    },
    "CloudWatch": {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazoncloudwatch.html"
    },

    "DynamoDb": {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazondynamodb.html"
    },
    "Glacier": {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonglacier.html",
    },
    "OpsWorks": {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awsopsworks.html"
    },
    "Sns": {
        "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonsns.html"
    },

    # Not implemented

    # "AppSync": {
    #     "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awsappsync.html"
    # },

    # "CloudTrail": {
    #     "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awscloudtrail.html"
    # },

    # "Cognito": {
    #     "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazoncognitouserpools.html",
    # },

    # "Rds": {
    #     "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonrds.html"
    # },

    # "Sqs": {
    #     "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonsqs.html",
    # },

    # "Neptune": {
    #     "URL": "https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonneptune.html"
    # },

}

Errors = set()

for service, values in Services.items():

    html = requests.get(values["URL"])
    URLs = [link for link in BeautifulSoup(
        html.text, features="lxml").find_all('a')]

    for table in pandas.read_html(html.content):

        # Defines all the substrings that must exist for the
        # record to be considered a match

        definition = {
            'Action': '',
            'Resource': '',
            'Description': '',
            'Access Level': ''
        }

        records = table.to_dict('records')

        if len(records) == 0:
            continue

        # One of the keys must include action and the other resource

        for k in definition.keys():
            definition[k] = next(
                (v for v in records[0].keys() if k.lower() in str(v).lower()), '')
            if definition[k] == '':
                break

        if any([v == '' for v in definition.values()]):
            continue

        Services[service]["Actions"] = {}
        for r in records:

            action = f"{service.lower()}:{r[definition['Action']].split()[0]}"

            # Normalise data

            data = {
                k if k not in definition.values()
                else [x for x, y in definition.items() if y == k][0]: v if str(v).lower() != "nan" else ''
                for k, v in r.items() if k != definition['Action']
            }

            # Ammend Specific (Non-Compulsory) Keys

            if "Condition Keys" in data and isinstance(data["Condition Keys"], str):
                data["Condition Keys"] = data["Condition Keys"].split()

            if "Dependent Actions" in data and isinstance(data["Dependent Actions"], str):
                data["Dependent Actions"] = data["Dependent Actions"].split()

            # Update resources

            resources = set()
            for a in [f"AWS::{service if service != 'Sts' else 'Iam'}::" +
                      ''.join(list(map(
                          lambda x: x[0].capitalize() +
                          # Lazy fix for stack change set
                          x[1:].replace("set", "Set"),
                          str(x).replace("-", " ").split()
                      ))) for x in data["Resource"].split(' ') if x != '']:

                matches = list(filter(
                    re.compile(a.replace('*', '(.*)')).match,
                    RESOURCES.types.keys())) if '*' in a else [a]

                if len(matches) == 0 or not all([m in RESOURCES.types.keys() for m in matches]):
                    Errors.update([f"Resource: {a}: was not matched "])
                    if "Missing Resources" not in Services[service]:
                        Services[service]["Missing Resources"] = []
                    Services[service]["Missing Resources"] = list(
                        set(Services[service]["Missing Resources"] + [a]))
                    continue

                resources.update(matches)

            urls = [link.get('href') for link in URLs if str(
                link.text).strip() == r[definition['Action']]]
            url = urls[0] if len(urls) == 1 else ''

            if url == '':
                Errors.update([f"Reference: Couldn't find a URL for {action}"])

            data = {
                "Affects": list(resources),
                "Access": data["Access Level"].title(),
                "Description": " ".join(data["Description"].split()),
                "Reference": url,
                **{k: v for k, v in data.items() if k not in ["Resource", "Access Level", "Description"]}
            }

            if action in Services[service]["Actions"]:

                for k, v in data.items():
                    if isinstance(v, list):
                        data[k] = list(
                            set(Services[service]["Actions"][action][k] + v))
                    elif isinstance(v, str) and v == "":
                        data[k] = Services[service]["Actions"][action][k]

            if data["Access"] == "":
                Errors.update(
                    [f"Access: empty access string for {action}, skipping action"])
                continue

            # Add Action to Services

            Services[service]["Actions"][action] = data

print("ACTIONS =", json.dumps({k: v for values in Services.values()
                  for k, v in values["Actions"].items()},
                 indent=2,
                 sort_keys=True))

# if len(Errors) > 0:
#     print("\nThere were a few problems:")
#     print('\n\t' + '\n\t'.join(sorted(list(Errors))))
