#from django.db import models
import couchdbkit.ext.django.schema as cdb
import datetime



class Datasource(cdb.Document):

    name = cdb.StringProperty()
    provides = cdb.ListProperty()
    
    
    def __unicode__(self):
        return "<cdb.document.Datasource id:%s, name:%s>" % (self._id, self.name)

    def __repr__(self):
        return self.__unicode__()
        

class Lens(cdb.Document):
    '''This is one single lens
    '''
    
    names = cdb.ListProperty()
    metadata = cdb.DictProperty()
    data = cdb.DictProperty()
    
    created_at = cdb.DateTimeProperty(default=datetime.datetime.utcnow())
    updated_at = cdb.DateTimeProperty(default=datetime.datetime.utcnow(), auto_now=True)
    
    created_by = cdb.StringProperty(default="")