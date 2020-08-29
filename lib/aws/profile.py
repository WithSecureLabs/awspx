
import sys
import os
from awscli.clidriver import CLIDriver, load_plugins
from awscli.customizations.configure.configure import ConfigureCommand
from awscli.customizations.configure import mask_value
from botocore.session import Session
from configparser import ConfigParser


class InteractivePrompter(object):

    def __init__(self, console):
        self.console = console

    def input(self, prompt, value):
        return self.console.input(f"{prompt} [{value}]: ")

    # See awscli/customizations/configure/configure.py

    def get_value(self, current_value, config_name, prompt_text=''):
        if config_name in ('aws_access_key_id', 'aws_secret_access_key'):
            current_value = mask_value(current_value)
        response = self.input(prompt_text, current_value)
        if not response:
            # If the user hits enter, we return a value of None
            # instead of an empty string.  That way we can determine
            # whether or not a value has changed.
            response = None
        return response


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

    def __init__(self, console=None):

        if console is None:
            from lib.util.console import console
        self.console = console

        self.credentials.read(self.credentials_file)
        self.config.read(self.config_file)

    def create(self, profile=None):
        self.reconfigure(profile)

    def reconfigure(self, profile=None):

        if profile is None:
            return

        # See awscli/clidriver.py
        session = Session()
        load_plugins(session.full_config.get('plugins', {}),
                     event_hooks=session.get_component('event_emitter'))

        driver = CLIDriver(session=session)
        driver._command_table = driver._build_command_table()
        driver._command_table["configure"] = ConfigureCommand(
            session,
            prompter=InteractivePrompter(self.console)
        )

        driver.main(args=["configure", "--profile", profile])

    def list(self):

        self.console.list([{"Profile": p} for p in self.credentials.keys()
                           if p != "DEFAULT"])

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

        self.console.info(f"Profile '{profile}' deleted.")
