
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

    resource = '(AWS(::[A-Za-z0-9-]*){1,2})'
    integer = '(^|\s)([\(]?)([0-9]+)([.\)])?(\s|$)'
    archive = '((/opt/awspx/data/)?[0-9]+_[A-Za-z0-9]+.zip)'
    database = '([A-Za-z0-9]+.db)'
    arn = '(arn(:[{}A-Za-z0-9-_/.]*){5})'
