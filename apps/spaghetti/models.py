# from django.db import models

# Create your models here.

from django.db import models

import couchdbkit.ext.django.schema as cdb

class TestDoc(cdb.Document):
    name = cdb.StringProperty()