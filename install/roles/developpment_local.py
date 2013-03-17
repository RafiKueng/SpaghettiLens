
# import the corresponding modules

from ..modules.database.sqlite import *
from lmt.settings.modules.django.dev import *
from lmt.settings.modules.static.xamp import *
from lmt.settings.modules.worker.dummy import *


# set some role specific settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG
