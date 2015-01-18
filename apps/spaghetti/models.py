# from django.db import models

# Create your models here.

from django.db import models

import couchdbkit.ext.django.schema as cdb

class TestDoc(cdb.Document):
    name = cdb.StringProperty()
    blaa = cdb.StringProperty()
    
    def __unicode__(self):
        return "<u spaghetti.models.TestDoc name:%s>" % self.name

#    def __str__(self):
#        return "<s spaghetti.models.TestDoc name:%s>" % self.name
        
    def __repr__(self):
        return "<r spaghetti.models.TestDoc name:%s>" % self.name
        
        


class Model(cdb.Document):
    pass
