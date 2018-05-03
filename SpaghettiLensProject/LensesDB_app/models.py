# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models
import datetime as DT
import mongoengine as me

# Create your models here.

class Datasource(me.Document):
    
    name     = me.StringField()
    provides = me.ListField(me.StringField())


    def __unicode__(self):
        return "<mongoengine.document.Datasource id:%s, name:%s>" % (self._id, self.name)

    def __repr__(self):
        return self.__unicode__()


class Lens(me.Document):
    '''This is one single lens
    '''
    
    names          = me.ListField(me.StringField())
    
    scidata        = me.DictField()
    imgdata        = me.DictField()
    metadata       = me.DictField()
    
    created_at     = me.DateTimeField(default=DT.datetime.utcnow)
    last_edited_at = me.DateTimeField(default=DT.datetime.utcnow)
    
    created_by     = me.StringField(default=None, null=True)
    edited_by      = me.ListField(me.StringField())
    
    
    def __unicode__(self):
        return "<mongoengine.document.Lens id:%s, name:%s>" % (self._id, self.names[0])

    def __repr__(self):
        return self.__unicode__()
