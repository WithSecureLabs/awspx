#!/usr/bin/python3

import argparse
import boto3

import git
import os
import sys

from botocore.credentials import InstanceMetadataProvider
from botocore.exceptions import ClientError
from botocore.utils import InstanceMetadataFetcher

from lib.aws.attacks import Attacks
from lib.aws.ingestor import *
from lib.aws.resources import RESOURCES
from lib.aws.profile import Profile
from lib.graph.db import Neo4j
from lib.util.console import console

SERVICES = list(Ingestor.__subclasses__())


def handle_update(args):
    """
    awspx update
    """

    repo = git.Repo("/opt/awspx")
    head = repo.head.commit

    repo.remotes.origin.set_url("https://github.com/FSecureLABS/awspx.git")
    repo.git.reset('--hard')
    repo.remotes.origin.pull()

    if head == repo.head.commit:
        console.notice("Already up to date")
        return

    console.task(f"Updating to {repo.head.commit}", os.system, args=[
                 "cd /opt/awspx/www && npm install >/dev/null 2>&1"],
                 done=f"Updated to {repo.head.commit}")


def handle_profile(args, console=console):
    """
    awspx profile
    """

    profile = Profile(console=console)

    if args.create_profile:
        profile.create(args.create_profile)
        if args.profile in Profile().credentials.sections():
            console.notice(f"Saved profile '{args.create_profile}'")
        else:
            sys.exit()

    elif args.list_profiles:
        profile.list()

    elif args.delete_profile:
        profile.delete(args.delete_profile)


def handle_ingest(args):
    """
    awspx ingest
    """

    session = None

    # Get credentials from environment variables
    if args.env:
        session = boto3.session.Session(region_name=args.region)

    # Use existing profile
    elif args.profile in Profile().credentials.sections():
        session = boto3.session.Session(profile_name=args.profile,
                                        region_name=args.region)
    # Use instance profile
    elif args.profile == "default":
        try:
            provider = InstanceMetadataProvider(
                iam_role_fetcher=InstanceMetadataFetcher())
            creds = provider.load()

            session = boto3.session.Session(region_name=args.region,
                                            aws_access_key_id=creds.access_key,
                                            aws_secret_access_key=creds.secret_key,
                                            aws_session_token=creds.token)
        except:
            pass

    # Specified profile doesn't exist, offer to create it
    if not session:

        profile = console.item("Create profile")
        profile.notice(f"The profile '{args.profile}' doesn't exist. "
                       "Please enter your AWS credentials.\n"
                       "(this information will be saved automatically)")

        args.create_profile = args.profile
        handle_profile(args, console=profile)

        session = boto3.session.Session(profile_name=args.profile,
                                        region_name=args.region)
    # Ancillary operations
    try:

        if args.mfa_device:

            session_token = session.client('sts').get_session_token(
                SerialNumber=args.mfa_device,
                TokenCode=args.mfa_token,
                DurationSeconds=args.mfa_duration
            )["Credentials"]

            session = boto3.session.Session(
                aws_access_key_id=session_token["AccessKeyId"],
                aws_secret_access_key=session_token["SecretAccessKey"],
                aws_session_token=session_token["SessionToken"],
                region_name=args.region)

        if args.role_to_assume:

            assumed_role = session.client('sts').assume_role(
                RoleArn=args.role_to_assume,
                RoleSessionName=f"awspx",
                DurationSeconds=args.role_to_assume_duration
            )["Credentials"]

            session = boto3.session.Session(
                aws_access_key_id=assumed_role["AccessKeyId"],
                aws_secret_access_key=assumed_role["SecretAccessKey"],
                aws_session_token=assumed_role["SessionToken"],
                region_name=args.region)

    except ClientError as e:
        console.critical(e)

    ingestor = IngestionManager(session=session, console=console, services=args.services,
                                db=args.database, quick=args.quick, skip_actions=args.skip_actions_all,
                                only_types=args.only_types, skip_types=args.skip_types,
                                only_arns=args.only_arns, skip_arns=args.skip_arns)

    assert ingestor.zip is not None, "Ingestion failed"

    args.load_zips = [ingestor.zip]
    handle_db(args, console=console.item("Creating Database"))

    if not (args.skip_attacks_all or args.skip_actions_all):
        handle_attacks(args, console=console.item("Updating Attack paths"))


def handle_attacks(args, console=console):
    """
    awspx attacks
    """

    attacks = Attacks(skip_conditional_actions=args.include_conditional_attacks == False,
                      skip_attacks=args.skip_attacks, only_attacks=args.only_attacks,
                      console=console)

    attacks.compute(max_iterations=args.max_attack_iterations,
                    max_search_depth=str(args.max_attack_depth
                                         if args.max_attack_depth is not None
                                         else ""))


def handle_db(args, console=console):
    """
    awspx db
    """

    db = Neo4j(console=console)

    if args.load_zips:

        db.load_zips(archives=args.load_zips,
                     db=args.database if 'database' in args else 'default.db')

    elif args.list_dbs:
        db.list()

    elif args.use_db:
        db.use(args.use_db)


def main():

    def profile(p):
        if p in list(Profile().credentials.sections()):
            raise argparse.ArgumentTypeError(f"profile '{p}' already exists")
        return p

    def service(service):
        match = next((s for s in SERVICES
                      if s.__name__.upper() == service.replace(',', '').upper()
                      ), None)
        if match is None:
            raise argparse.ArgumentTypeError(
                f"'{service}' is not a supported service "
                f"(eg: {', '.join([str(v.__name__) for v in SERVICES])})")
        return match

    def resource(resource):

        match = next((r for r in RESOURCES
                      if r.upper() == resource.upper()
                      ), None)
        if match is None:
            raise argparse.ArgumentTypeError(
                f"'{resource}' is not a supported resource type "
                "(see lib/aws/resources.py for details)")
        return match

    def ARN(arn):

        if re.compile(
            "arn:aws:([a-zA-Z0-9]+):([a-z0-9-]*):(\d{12}|aws)?:(.*)"
        ).match(arn) is None:
            raise argparse.ArgumentTypeError(
                f"'{arn}' is not a valid ARN")

        return arn

    def attack(name):
        match = next((a for a in Attacks.definitions
                      if a.upper() == name.upper()
                      ), None)
        if match is None:
            raise argparse.ArgumentTypeError(
                f"'{name}' is not a supported attack "
                '(see lib/aws/attacks.py for details)')
        return match

    parser = argparse.ArgumentParser(
        prog="awspx",
        description=("awspx is a graph-based tool for visualizing effective "
                     "access and resource relationships within AWS. "))

    subparsers = parser.add_subparsers(title="commands")

    #
    # awspx update
    #
    update_parser = subparsers.add_parser("update",
                                          help="Update awspx to the latest version.")
    update_parser.set_defaults(func=handle_update)

    #
    # awspx profile
    #
    profile_parser = subparsers.add_parser("profile",
                                           help="Manage AWS credential profiles used for ingestion.")
    profile_parser.set_defaults(func=handle_profile)

    profile_group = profile_parser.add_mutually_exclusive_group(required=True)

    profile_group.add_argument('--create', dest='create_profile', default=None, type=profile,
                               help="Create a new profile using `aws configure`.")
    profile_group.add_argument('--list', dest='list_profiles', action='store_true',
                               help="List saved profiles.")
    profile_group.add_argument('--delete', dest='delete_profile', choices=Profile().credentials.sections(),
                               help="Delete a saved profile.")
    #
    # awspx ingest
    #
    ingest_parser = subparsers.add_parser(
        "ingest", help="Ingest data from an AWS account.")
    ingest_parser.set_defaults(func=handle_ingest)

    # Profile & region args
    pnr = ingest_parser.add_argument_group("Profile and region")
    pnr.add_argument('--env', action='store_true',
                     help="Use AWS credential environment variables.")
    pnr.add_argument('--profile', dest='profile', default="default",
                     help="Profile to use for ingestion (corresponds to a `[section]` in `~/.aws/credentials).")
    pnr.add_argument('--mfa-device', dest='mfa_device',
                     help="ARN of the MFA device to authenticate with.")
    pnr.add_argument('--mfa-token', dest='mfa_token',
                     help="Current MFA token.")
    pnr.add_argument('--mfa-duration', dest='mfa_duration', type=int, default=3600,
                     help="Maximum session duration in seconds (for MFA session).")
    pnr.add_argument('--assume-role', dest='role_to_assume',
                     help="ARN of a role to assume for ingestion (useful for cross-account ingestion).")
    pnr.add_argument('--assume-role-duration', dest='role_to_assume_duration', type=int, default=3600,
                     help="Maximum session duration in seconds (for --assume-role).")
    pnr.add_argument('--region', dest='region', default="eu-west-1", choices=Profile.regions,
                     help="Region to ingest (defaults to profile region, or `eu-west-1` if not set).")
    pnr.add_argument('--database', dest='database', default=None,
                     help="Database to store results (defaults to <profile>.db).")

    # Services & resources args
    snr = ingest_parser.add_argument_group("Services and resources")
    snr.add_argument('--services', dest='services', default=SERVICES, nargs="+", type=service,
                     help=(f"One or more services to ingest (eg: {' '.join([s.__name__ for s in SERVICES])})."))
    snr.add_argument('--quick', dest='quick', action='store_true', default=False,
                     help=("Skips supplementary ingestion functions "
                           "(i.e. speed at the cost of infromation)."))

    type_args = snr.add_mutually_exclusive_group()
    type_args.add_argument('--only-types', dest='only_types', default=[], nargs="+", type=resource,
                           help="Resource to include by type, all other resource types will be excluded.")
    type_args.add_argument('--skip-types', dest='skip_types', nargs="+", default=[],
                           type=resource, help="Resources to exclude by type.")

    # ARN args
    arn_args = snr.add_mutually_exclusive_group()
    arn_args.add_argument('--only-arns', dest='only_arns', default=[], nargs="+", type=ARN,
                          help="Resources to include by ARN, all other resources will be excluded.")
    arn_args.add_argument('--skip-arns', dest='skip_arns', default=[], nargs="+", type=ARN,
                          help="Resources to exclude by ARN.")

    actions = ingest_parser.add_argument_group("Actions")
    actions.add_argument('--skip-actions-all', dest='skip_actions_all', action='store_true', default=False,
                         help="Skip policy resolution (actions will not be processed).")

    #
    # awspx attacks
    #
    attacks_parser = subparsers.add_parser("attacks",
                                           help="Compute attacks using the active database.")
    attacks_parser.set_defaults(func=handle_attacks)

    # Add args to ingest, attacks
    for p in [ingest_parser, attacks_parser]:
        ag = p.add_argument_group("Attack computation")
        g = ag.add_mutually_exclusive_group()

        g.add_argument('--skip-attacks', dest='skip_attacks', default=[], nargs="+", type=attack,
                       help="Attacks to exclude by name.")
        g.add_argument('--only-attacks', dest='only_attacks', default=[], nargs="+", type=attack,
                       help="Attacks to include by name, all other attacks will be excluded.")
        ag.add_argument('--max-attack-iterations', dest='max_attack_iterations', default=5, type=int,
                        help="Maximum number of iterations to run each attack (default: 5).")
        ag.add_argument('--max-attack-depth', dest='max_attack_depth', default=None, type=int,
                        help="Maximum search depth for attacks (default: None).")
        ag.add_argument('--include-conditional-attacks', dest='include_conditional_attacks', action='store_true', default=False,
                        help="Include conditional actions when computing attacks (default: False).")

        if p is ingest_parser:
            ag.add_argument('--skip-attacks-all', dest='skip_attacks_all', action='store_true', default=False,
                            help="Skip attack path computation (it can be run later with `awspx attacks`).")

    #
    # awspx db
    #
    db_parser = subparsers.add_parser(
        "db", help="Manage databases used for visualization, ingestion, and attack computation.")

    db_parser.set_defaults(func=handle_db)

    db_group = db_parser.add_mutually_exclusive_group(required=True)

    db_group.add_argument('--use', dest='use_db', choices=Neo4j.databases,
                          help="Switch to the specified database.")
    db_group.add_argument('--list', dest='list_dbs', action='store_true',
                          help="List available databases.")
    db_group.add_argument('--load-zip', dest='load_zips', choices=sorted(Neo4j.zips), action='append',
                          help="Create/overwrite database using ZIP file content.")

    # Add --verbose to ingest, attacks, db
    for p in [ingest_parser, attacks_parser, db_parser]:
        p.add_argument('--verbose', dest='verbose', action='store_true', default=False,
                       help="Enable verbose output.")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Unless a database has been defined for ingest, default to <profile>.db
    if 'database' in args and args.database is None:
        args.database = f"{args.profile}.db"

    if 'verbose' in args and args.verbose:
        console.verbose()
    else:
        console.start()

    try:
        args.func(args)

    except (KeyboardInterrupt, SystemExit):
        console.stop()
        os._exit(1)

    except BaseException as e:
        console.critical(e)
        os._exit(1)

    console.stop()


main()
