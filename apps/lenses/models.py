#from django.db import models
import couchdbkit.ext.django.schema as cdb



class Datasource(cdb.Document):

    name = cdb.StringProperty()
    provides = cdb.ListProperty()
    
    
    def __unicode__(self):
        return "<cdb.document.Datasource id:%s, name:%s>" % (self._id, self.name)

    def __repr__(self):
        return self.__unicode__()
        
