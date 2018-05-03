# from django.db import models

# Create your models here.

import datetime

#from django.db import models
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
    
    lens_id = cdb.StringProperty()
    parent = cdb.StringProperty()
    
    created_by = cdb.StringProperty()
    created_at = cdb.DateTimeProperty(default=datetime.datetime.utcnow())
    comments = cdb.ListProperty(default=[])
    checksum = cdb.StringProperty()
    
    obj = cdb.DictProperty()
    glass = cdb.DictProperty()

    task_id = cdb.StringProperty()
    rendered = cdb.BooleanProperty()
    isFinal = cdb.BooleanProperty()
    
    def __unicode__(self):
        return "<u spaghetti.models.Model id:%s-%s>" % (self._id[0:5], self._id[5:])


