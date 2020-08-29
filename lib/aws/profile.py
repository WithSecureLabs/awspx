
import sys
import os
from configparser import ConfigParser


class Profile:

    regions = [
        "af-south-1", "ap-east-1", "ap-northeast-1",
        "ap-northeast-2", "ap-northeast-3", "ap-south-1",
        "ap-southeast-1", "ap-southeast-2", "ca-central-1",
        "cn-north-1", "cn-northwest-1", "eu-central-1",
        "eu-north-1", "eu-south-1", "eu-west-1",
        "eu-west-2", "eu-west-3", "me-south-1",
        "sa-east-1",  "us-east-1", "us-east-2",
        "us-gov-east-1", "us-gov-west-1", "us-west-1",
        "us-west-2"
    ]

    config_file = os.environ['HOME'] + '/.aws/config'
    credentials_file = os.environ['HOME'] + '/.aws/credentials'

    config = ConfigParser()
    credentials = ConfigParser()

    def __init__(self):

        self.credentials.read(self.credentials_file)
        self.config.read(self.config_file)

    def create(self, profile=None):
        self.reconfigure(profile)

    def reconfigure(self, profile=None):

        os.system(f"aws configure --profile {profile}")
        try:
            print(f"[+] Profile '{profile}' successfully created. "
                  f"(identity: {identity['Arn']}).\n")
        except:
            print(f"[+] Profile '{profile}' created.")

    def list(self):

        for profile in [p for p in self.credentials.keys()
                        if p != "DEFAULT"]:
            print(profile)

    def delete(self, profile=None):

        if profile is None:
            return

        if self.config.has_section(profile):
            self.config.remove_section(profile)

        if self.credentials.has_section(profile):
            self.credentials.remove_section(profile)

        with open(self.config_file, 'w') as f:
            self.config.write(f)

        with open(self.credentials_file, 'w') as f:
            self.credentials.write(f)

        print(f"[+] Profile '{profile}' deleted.")
