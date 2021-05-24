
from lib.aws.attacks import definitions
from lib.aws.ingestor import *
from lib.aws.profile import Profile
from lib.aws.actions import ACTIONS
from lib.aws.resources import Resources
from lib.graph.edges import *
from lib.graph.nodes import *


class Keywords:

    service = [_.__name__ for _ in Ingestor.__subclasses__()]
    resource = [k.split(':')[-1] for k in Resources.types]
    node = [_.__name__ for _ in Node.__subclasses__()]
    edge = [_.__name__ for _ in Edge.__subclasses__()]
    region = list(Profile.regions)
    action = list(ACTIONS.keys())
    attack = list(definitions.keys())


class Regex:

    arn = r'arn:aws:([a-z0-9]+):({Region}|[a-z0-9-]*):({Account}|[0-9]{12}|aws)?:([a-z0-9-]+)([A-Za-z0-9-_\.:/{}]+)?'
    resource = r'(AWS(::[A-Za-z0-9-]*){1,2})'
    integer = r'[0-9]+'
    archive = r'((/opt/awspx/data/)?[0-9]+_[A-Za-z0-9]+.zip)'
    database = r'([A-Za-z0-9]+.db)'
