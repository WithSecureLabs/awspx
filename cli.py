#!/usr/bin/python3

import argparse
import csv
import os
import sys
from configparser import ConfigParser
from random import randrange

import boto3
from botocore.exceptions import ProfileNotFound

from lib.aws.attacks import Attacks
from lib.aws.ingestor import *
from lib.aws.resources import RESOURCES
from lib.graph.base import Elements
from lib.graph.db import Neo4j

SERVICES = list(Ingestor.__subclasses__())
REGIONS = [
    "us-east-2",
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "ap-south-1",
    "ap-northeast-3",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "cn-north-1",
    "cn-northwest-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-north-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
]

CREDENTIALS = ConfigParser()
CONFIG = ConfigParser()

PATH = os.path.dirname(__file__)  # for functions that use relative paths
AWS_DIR = os.environ['HOME'] + '/.aws/'
CREDENTIALS_FILE = os.environ['HOME'] + '/.aws/credentials'
CONFIG_FILE = os.environ['HOME'] + '/.aws/config'


def profile(args):
    """
    awspx profile
    """
    CREDENTIALS.read(CREDENTIALS_FILE)
    CONFIG.read(CONFIG_FILE)

    if args.list_profiles:
        profiles = list(CREDENTIALS.keys())
        profiles.remove('DEFAULT')
        print("\n".join(profiles))

    elif args.create_profile:
        os.system(f"aws configure --profile {args.create_profile}")
        session = boto3.session.Session(profile_name=args.create_profile)
        identity = session.client('sts').get_caller_identity()

        print(f"[+] Profile created. User is {identity['Arn']}.")
        return True
    elif args.delete_profile:
        if CONFIG.has_section(args.delete_profile):
            CONFIG.remove_section(args.delete_profile)
        if CREDENTIALS.has_section(args.delete_profile):
            CREDENTIALS.remove_section(args.delete_profile)
            print(f"[+] Profile '{args.delete_profile}' deleted.")
        else:
            print(f"[-] Profile '{args.delete_profile}' does not exist.")

    with open(CONFIG_FILE, 'w') as f:
        CONFIG.write(f)

    with open(CREDENTIALS_FILE, 'w') as f:
        CREDENTIALS.write(f)


def ingest(args):
    """
    awspx ingest
    """

    account = "0000000000000"
    ingested = Elements()
    iam = None

    profile = args.profile if args.profile else "default"

    # offer to create profile it doesn't exist
    try:
        session = boto3.session.Session(profile_name=profile)
    except ProfileNotFound:
        create_new_profile(profile)
        session = boto3.session.Session(profile_name=profile)

    if not args.region:
        r = boto3.session.Session(profile_name=profile).region_name
        region = r if r != None else "eu-west-1"
    else:
        region = args.region

    if not args.database:
        database = profile+".db"
    else:
        if args.database[-3:] == ".db":
            database = args.database
        else:
            database = args.database+".db"

    if args.services and args.services != "all":
        services = [s for s in SERVICES if s.__name__.upper() in map(
            str.upper, args.services.strip(" ").split(','))]
    else:
        services = SERVICES

    # Always ingest IAM
    if IAM not in services:
        services.insert(0, IAM)

    # Resolve only & except resources types & ARNs
    optional_resource_args = ""
    selections = {}
    if args.except_types:
        selections["except_types"] = args.except_types.split(",")
        validate_types(selections["except_types"])
        optional_resource_args = optional_resource_args + \
            f"                     --except-types {args.except_types} \\\n"
    else:
        selections["except_types"] = []

    if args.only_types:
        selections["only_types"] = args.only_types.split(",")
        validate_types(selections["only_types"])
        optional_resource_args = optional_resource_args + \
            f"                     --only-types {args.only_types} \\\n"
    else:
        selections["only_types"] = []

    if args.except_arns:
        selections["except_arns"] = args.except_arns.lower().split(",")
        optional_resource_args = optional_resource_args + \
            f"                     --except-arns {args.except_arns} \\\n"
    else:
        selections["except_arns"] = []

    if args.only_arns:
        selections["only_arns"] = args.only_arns.lower().split(",")
        optional_resource_args = optional_resource_args + \
            f"                     --only-arns {args.only_arns} \\\n"
    else:
        selections["only_arns"] = []

    if args.role_to_assume:
        assume_role_arg = f"                     --assume-role {args.role_to_assume} \\\n"
    else:
        assume_role_arg = ""

    max_attack_iterations, max_attack_depth, ignore_conditionals, except_attacks, only_attacks = attacks(
        args)

    if args.skip_attacks:
        attack_args = "                     --skip-attacks"
    else:
        attack_args = f"""                     --max-attack-iterations {str(max_attack_iterations)} \\
                     --ignore-conditionals {str(ignore_conditionals)} \\
    """

        if max_attack_depth != "":
            attack_args = attack_args + \
                f"                     --max-attack-depth {max_attack_depth} \\"

        if except_attacks:
            attack_args = attack_args + \
                f"                 --except-attacks {','.join(except_attacks)}"
        elif only_attacks:
            attack_args = attack_args + \
                f"                 --only-attacks {','.join(only_attacks)}"

    print(f"""
[+] Running awspx ingest --profile {profile} --region {region} --database {database} \\
                     --services {','.join([s.__name__ for s in services])} \\
{assume_role_arg+optional_resource_args+attack_args}
          """)

    try:
        session = boto3.session.Session(
            profile_name=profile, region_name=region)
        identity = session.client('sts').get_caller_identity()
        account = identity["Account"]
        print(f"[+] User set to {identity['Arn']}.")
        print(f"[+] Region set to {region}.")
    except:
        print("[-] Request to establish identity (sts:GetCallerIdentity) failed.")

    if args.role_to_assume:
        response = session.client('sts').assume_role(
            RoleArn=args.role_to_assume,
            RoleSessionName=f"awspx",
            DurationSeconds=7200)
        if response:
            print(f"[+] Assumed role {args.role_to_assume}")
            session = boto3.session.Session(
                aws_access_key_id=response["Credentials"]["AccessKeyId"],
                aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
                aws_session_token=response["Credentials"]["SessionToken"],
                region_name=region)
        try:
            identity = session.client('sts').get_caller_identity()
            account = identity["Account"]
            print(f"[+] Running as {identity['Arn']}.")
            print(f"[+] Region set to {region}.")
        except:
            print("[-] Request to establish identity (sts:GetCallerIdentity) failed.")

        if not args.database:
            database = f"{args.role_to_assume.split('::')[1].split(':')[0]}-{database}"

    print(f"[+] Using database {database}")

    if IAM in services:
        iam = IAM(session, db=database)
        account = iam.root.account()

    for service in [s for s in services if s != IAM]:
        resources = service(session, **selections, account=account)
        ingested += resources

    if IAM not in services:
        iam = IAM(session, db=database, resources=ingested)
    else:
        iam += ingested

    archive = iam.post()
    print(f"[+] Results exported to {archive}")
    Neo4j.load(archive, database)

    if not args.skip_attacks:
        print("[+] Computing attack paths")
        Attacks.compute(
            max_iterations=max_attack_iterations,
            except_attacks=except_attacks,
            only_attacks=only_attacks,
            max_search_depth=max_attack_depth,
            ignore_actions_with_conditions=ignore_conditionals
        )

    print("[+] Done.")


def attacks(args):
    """
    awspx attacks
    """
    max_attack_iterations = int(args.max_attack_iterations) \
        if args.max_attack_iterations else 5
    max_attack_depth = args.max_attack_depth \
        if args.max_attack_depth else ""
    ignore_conditionals = False \
        if args.include_conditionals else True

    # Resolve only & except attacks
    except_attacks = []
    if args.except_attacks:
        except_attacks = [k for k in Attacks.definitions.keys()
                          if k.lower() in args.except_attacks.lower()]

    only_attacks = []
    if args.only_attacks:
        only_attacks = [k for k in Attacks.definitions.keys()
                        if k.lower() in args.only_attacks.lower()]

    if args.func == attacks:
        print("[+] Computing attack paths")
        Attacks.compute(
            max_iterations=max_attack_iterations,
            except_attacks=except_attacks,
            only_attacks=only_attacks,
            max_search_depth=max_attack_depth,
            ignore_actions_with_conditions=ignore_conditionals
        )
    else:
        return max_attack_iterations, max_attack_depth, ignore_conditionals, except_attacks, only_attacks


def db(args):
    """
    awspx db
    """

    dbdir = "/data/databases/"

    if args.list_dbs:
        databases = [d for d in os.listdir(dbdir)
                     if os.path.isdir(os.path.join(dbdir, d))]
        print("\n".join(databases))

    elif args.use_db:
        if args.use_db[-3:] == ".db":
            d = args.use_db
        else:
            d = args.use_db + ".db"

        db = os.path.join(dbdir, d)
        if os.path.isdir(db):
            Neo4j.switch_database(db)
            Neo4j.restart()

        print(f"Switched to {db}.")

    elif args.load_zip:
        zips = [z for z in os.listdir("/opt/awspx/data")
                if args.load_zip in z]
        dbname = args.load_zip.replace(".zip", ".db")

        if zips:
            print(f"[+] Loading /opt/awspx/data/{zips[0]} into {dbname}.")
            Neo4j.load("/opt/awspx/data/"+zips[0], dbname)
        else:
            print(f"[-] {args.load_zip} not found in /opt/awpsx/data/.")


def loaded():
    """
    Fetch previously loaded resources and services from the database.
    """

    resources = [r["r"] for r in Neo4j.run(
        "MATCH (g:Generic) "
        "WITH [_ IN LABELS(g) "
        "WHERE _ <> 'Generic'][0] AS r "
        "RETURN r ORDER BY r")]

    services = [s for s in SERVICES if s.upper() in list(
        set([s.split('::')[1].upper() for s in resources]))]

    return {
        "Resources": resources,
        "Services": services
    }


def create_new_profile(profile_name):
    """
    Prompt user to create new profile with aws cli.
    """
    cn = input(
        f"[-] The profile \"{profile_name}\" was not found. Would you like to create it? (y/n) ")
    if 'y' in cn:
        os.system(f"aws configure --profile {profile_name}")
        return True
    elif 'n' in cn:
        sys.exit()


def validate_types(types):
    """
    Check types against known resources & print invalid ones.
    """

    invalid = set(types) - set(RESOURCES.keys())
    if invalid != set():
        print(f"Invalid resource type(s): {list(invalid)}.")
        sys.exit()


def main():

    parser = argparse.ArgumentParser(
        description=("Awspx is a proof-of-concept designed to support visualising "
                     "effective access and resource relationships in AWS environments."))

    subparsers = parser.add_subparsers(title="commands")

    #
    # awspx profile
    #
    profile_parser = subparsers.add_parser("profile", help="Manage AWS credential profiles.",
                                           description="Create, list and delete profiles for AWS ingestion.")
    profile_parser.set_defaults(func=profile)

    profile_group = profile_parser.add_mutually_exclusive_group(required=True)

    profile_group.add_argument('--create', dest='create_profile',
                               help="Create a new profile using aws configure.")
    profile_group.add_argument('--list', dest='list_profiles', action='store_true',
                               help="List profiles you have saved previously.")
    profile_group.add_argument('--delete', dest='delete_profile',
                               help="Delete a saved profile.")
    #
    # awspx ingest
    #
    ingest_parser = subparsers.add_parser("ingest", help="Ingest data from an AWS account.",
                                          description="Ingest resources from supported services.")
    ingest_parser.set_defaults(func=ingest)

    # Profile & region args
    pnr = ingest_parser.add_argument_group("Profile and region")
    pnr.add_argument('--profile', dest='profile',
                     help="Profile to use for ingestion. Corresponds to a [section] in ~/.aws/credentials.")
    pnr.add_argument('--assume-role', dest='role_to_assume',
                     help="ARN of role to assume for ingestion. Useful for cross-account ingestion.")
    pnr.add_argument('--region', dest='region',
                     help="Region to ingest (defaults to profile region, else eu-west-1).")
    pnr.add_argument('--database', dest='database',
                     help="Name of database to use (defaults to <profile-name>.db).")

    # Services & resources args
    snr = ingest_parser.add_argument_group("Services and resources")
    snr.add_argument('--services', dest='services',
                     help=("Comma-separated list of services to ingest. Supported: IAM, EC2, S3, Lambda. "
                           "IAM will be run regardless of whether it is included here."))

    # Type args
    type_args = snr.add_mutually_exclusive_group()
    type_args.add_argument('--only-types', dest='only_types',
                           help=("Comma-separated list of resource types to include. "
                                 "No others will be ingested. For example, "
                                 "'AWS::S3::Object,AWS::EC2::Instance' will include S3 objects and EC2 instances. "
                                 "See lib/aws/resources.py for all known types."))
    type_args.add_argument('--except-types', dest='except_types',
                           help=("Comma-separated list of resource types to exclude. "
                                 "For example, 'AWS::S3::Object,AWS::EC2::Instance' will exclude S3 objects "
                                 "and EC2 instances. See lib/aws/resources.py for all known types."))

    # ARN args
    arn_args = snr.add_mutually_exclusive_group()
    arn_args.add_argument('--only-arns', dest='only_arns',
                          help="Comma-separated list of resource ARNs to include. No others will be ingested.")
    arn_args.add_argument('--except-arns', dest='except_arns',
                          help="Comma-separated list of resource ARNS to exclude.")

    #
    # awspx attacks
    #
    attacks_parser = subparsers.add_parser("attacks", help="Compute attacks on current awspx database.",
                                           description="Compute attacks for current database.")
    attacks_parser.set_defaults(func=attacks)

    for p in [ingest_parser, attacks_parser]:  # add args to both
        ag = p.add_argument_group("Attack computation")
        g = ag.add_mutually_exclusive_group()

        g.add_argument('--except-attacks', dest='except_attacks',
                       help="Comma-separated list of attacks to exclude.")
        g.add_argument('--only-attacks', dest='only_attacks',
                       help="Comma-separated list of attacks to include. No others will be computed.")

        ag.add_argument('--max-attack-iterations', dest='max_attack_iterations',
                        help="Maximum number of iterations to run each attack.")
        ag.add_argument('--max-attack-depth', dest='max_attack_depth',
                        help="Maximum search depth for attacks.")
        ag.add_argument('--include-conditionals', dest='include_conditionals', action='store_true',
                        help="Include policy statements with conditionals when computing attacks.")

        if p is ingest_parser:
            ag.add_argument('--skip-attacks', dest='skip_attacks', action='store_true',
                            help="Skip attack path computation. You can run that later with awspx attacks.")

    #
    # awspx db
    #
    db_parser = subparsers.add_parser("db", help="Manage awspx databases.",
                                      description="Choose which database to view and load new databases from CSVs.")
    db_parser.set_defaults(func=db)

    db_group = db_parser.add_mutually_exclusive_group(required=True)

    db_group.add_argument('--use', dest='use_db',
                          help="Use an existing Neo4j database.")
    db_group.add_argument('--list', dest='list_dbs', action='store_true',
                          help="List Neo4j databases.")
    db_group.add_argument('--load-zip', dest='load_zip',
                          help="Create a new database from an awspx zip file. Zips must be located in /opt/awspx/data/.")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


main()
