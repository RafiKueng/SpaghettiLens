# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db import models as fields
#from django.contrib.postgres import fields as fields_pg

# from django.contrib.postgres.fields import ArrayField, JSONField

import datetime as DT
import os
import hashlib


HASH_FUNC = hashlib.sha256


def get_hash(lens_model_instance):
    hashfn = HASH_FUNC()
    for data in lens_model_instance.file.chunks():
        hashfn.update(data)
    digest = hashfn.hexdigest()
    return digest
    

def hash_upload(lens_model_instance, orgfilename):    
    basefn, ext = os.path.splitext(orgfilename)
    digest = get_hash(lens_model_instance)
    filename = os.path.join('lenses', digest[0:2], digest[2:4], digest[4:], ext)
    return filename
    
    

class Lens(models.Model):
    '''This is one single lens'''
    
    hash = fields.CharField(unique=True, max_length=64)
    names = fields.TextField()
    file = fields.FileField(upload_to=hash_upload)
    
    scidata = fields.TextField()
    imgdata = fields.TextField()
#    metadata = fields.TextField()
    
    created_at = fields.DateTimeField(default=DT.datetime.utcnow)
    created_by = fields.TextField(default=None, null=True)

    edit_history = fields.TextField()


    def save(self):
        self.hash = get_hash(self)
        super(Lens, self).save()

    
    def __unicode__(self):
        return "<Lens hash:%s, names:'%s'>" % (self.hash, self.names)

    def __repr__(self):
        return self.__unicode__()




# import mongoengine as me
#
# me.connect(
#    db='test',
#    username='user',
#    password='12345',
#    host='mongodb://admin:qwerty@localhost/production'
# )
#
#
# class Datasource(me.Document):
#
#    name = me.StringField()
#    provides = me.ListField(me.StringField())
#
#    def __unicode__(self):
#        return "<mongoengine.document.Datasource id:%s, name:%s>" % (self._id, self.name)
#
#    def __repr__(self):
#        return self.__unicode__()
#
#
# class Lens(me.Document):
#    '''This is one single lens'''
#    
#    names = me.ListField(me.StringField())
#    
#    scidata = me.DictField()
#    imgdata = me.DictField()
#    metadata = me.DictField()
#    
#    created_at = me.DateTimeField(default=DT.datetime.utcnow)
#    last_edited_at = me.DateTimeField(default=DT.datetime.utcnow)
#    
#    created_by = me.StringField(default=None, null=True)
#    edited_by = me.ListField(me.StringField())
#    
#    def __unicode__(self):
#        return "<mongoengine.document.Lens id:%s, name:%s>" % (self._id, self.names[0])
#
#    def __repr__(self):
#        return self.__unicode__()

#
#class Datasource(models.Document):
#    '''This saves all the possible datasources'''
#    
#    # definition of source types
#    
#    UNDEFINED = 'UDEF'
#    COMPOSITE = 'COMP'
#    FITS      = 'FITS'
#    
#    TYPES_OF_DATASOURCES = (
#        (UNDEFINED, 'Someone was lazy here..'),
#        (COMPOSITE, 'Already composed multichannel rgb image'),
#        (FITS, 'FITS File containing whatever kind of data'),
#    )
#
#    name = fields.CharField(max_length=256)
#    desc = fields.TextField()
#
##    provides = fields_pg.ArrayField(
##        fields.CharField(
##            max_length=4,
##            choices=TYPES_OF_DATASOURCES,
##            default=UNDEFINED,
##        )
##    )
##    provides = fields.CharField(
##        max_length=4,
##        choices=TYPES_OF_DATASOURCES,
##        default=UNDEFINED,
##    )
#
#    def __unicode__(self):
#        return "<LensAPI.Datasource id:%s, name:%s>" % (self._id, self.name)
#
#    def __repr__(self):
#        return self.__unicode__()



# class Lens(me.Document):
#    '''This is one single lens'''
#    
#    names = me.ListField(me.StringField())
#    
#    scidata = me.DictField()
#    imgdata = me.DictField()
#    metadata = me.DictField()
#    
#    created_at = me.DateTimeField(default=DT.datetime.utcnow)
#    last_edited_at = me.DateTimeField(default=DT.datetime.utcnow)
#    
#    created_by = me.StringField(default=None, null=True)
#    edited_by = me.ListField(me.StringField())
#    
#    def __unicode__(self):
#        return "<mongoengine.document.Lens id:%s, name:%s>" % (self._id, self.names[0])
#
#    def __repr__(self):
#        return self.__unicode__()
#
