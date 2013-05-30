from django.db import models
from django.contrib.auth.models import User
from djcelery.models import TaskMeta

# Create your models here.

class LensData(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=200)
  
  datasource = models.CharField(max_length=200)
  datasource_id = models.CharField(max_length=200)
  
  img_data = models.TextField()
  add_data = models.TextField()

  n_res = models.IntegerField(blank=False, null=True, default=0) # how many finished results were uploaded?
  created = models.DateTimeField(auto_now_add=True) #when was it added
  created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)# by who was it added, for later use of user management
  created_by_str = models.CharField(max_length=200, blank=True) # ...now just use strings
  last_accessed = models.DateTimeField(blank=True, null=True) #when was it last accessed

  def __unicode__(self):
    return "LensdataN [id: %04i |name: %s | %s: %s]" % (
      self.id,
      self.name,
      self.datasource,
      self.datasource_id
    )


class Collection(models.Model):
  name =  models.CharField(max_length=32) #identifier
  description = models.CharField(max_length=300, blank=True) # further description
  
  lenses =  models.ManyToManyField(LensData)

  created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)# by who was it added
  created_by_str = models.CharField(max_length=200, blank=True)

  def __unicode__(self):
    return ''.join([
      'Catalog [ id: %02i | name: %s | descr: %s ]' % (
         self.pk,
         self.name,
         self.description if self.description else "-----" )])


class BasicLensData(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=200)
  
  # is this data part of a set (like castles)? enter some infos about it here
  catalog = models.ForeignKey('Catalog', blank=True, null=True, on_delete=models.SET_NULL)
  catalog_img_id = models.IntegerField(blank=True, null=True) # does it have an id in this set? store it here for reference
  
  # adiminstative fields
  n_res = models.IntegerField(blank=False, null=True, default=0) # how many finished results were uploaded?
  requested_last = models.DateTimeField(blank=True, null=True) #when was it last requested to work on?
  
  # if these are already known, enter them here
  z_lens = models.FloatField(blank=True, null=True)
  z_source = models.FloatField(blank=True, null=True)
  
  IMGTYPE_CHOICES = (
    ('BW', 'multi channels, each a grayscale image'),
    ('CO', 'multi channels, one single color image'),
  )
  BAND_CHOICES = (
    ('U', 'U: UV, 365nm'),
    ('B', 'B: blue, 445nm'),
    ('V', 'V: visual, 551nm'),
    ('G', 'G: green, 551nm'),
    ('R', 'R: red, 658nm'),
    ('I', 'I: nearIR, 806nm'),
    ('Z', 'Z: nearIR, 900nm'),
    ('Y', 'Y: nearIR, 1020nm'),
    ('J', 'J: nearIR, 1220nm'),
    ('H', 'H: nearIR, 1630nm'),
    ('K', 'K: nearIR, 2190nm'),
    ('L', 'L: nearIR, 3450nm'),
    ('M', 'M: midIR, 4750nm'),
    ('N', 'N: midIR, ????nm'),
    ('Q', 'Q: midIR, ????nm'),
  )
  
  img_type = models.CharField(max_length=2, choices=IMGTYPE_CHOICES)
  
  # if image type = grayscale multichannel, enter the information for each channel (up to 5)
  # if already a composite color image, just fill in the first channel url
  # data is a json object representing default values for color, brightness and contrast for this channel in the UI
  # r, g, b from 0..1, [co]ntrast from 0.1 .. 1 .. 10; [br]ightness from -1..0..1, see the UI for deatils
  # {"r": "1", g: 0, b:0, co: 1, br:0}
  channel1_imgurl = models.CharField(max_length=200)
  channel1_type = models.CharField(max_length=1, choices=BAND_CHOICES, blank=True)
  channel1_data = models.CharField(max_length=200, blank=True)
  
  channel2_imgurl = models.CharField(max_length=200, blank=True)
  channel2_type = models.CharField(max_length=1, choices=BAND_CHOICES, blank=True)
  channel2_data = models.CharField(max_length=200, blank=True)

  channel3_imgurl = models.CharField(max_length=200, blank=True)
  channel3_data = models.CharField(max_length=200, blank=True)
  channel3_type = models.CharField(max_length=1, choices=BAND_CHOICES, blank=True)

  channel4_imgurl = models.CharField(max_length=200, blank=True)
  channel4_data = models.CharField(max_length=200, blank=True)
  channel4_type = models.CharField(max_length=1, choices=BAND_CHOICES, blank=True)
  
  channel5_imgurl = models.CharField(max_length=200, blank=True)
  channel5_data = models.CharField(max_length=200, blank=True)
  channel5_type = models.CharField(max_length=1, choices=BAND_CHOICES, blank=True)
    
  # who has already modeled this dataset? a many to one relation ship
  modellers = models.ManyToManyField(User, through='ModellingSession')
    
  def __unicode__(self):
    return ''.join(['LensData [ id: ', "%04i" % self.pk,
                    ' | name: '      , self.name,
                    ' | catalog: '   , self.catalog.name if self.catalog else "-----",
                    ' | type: '      , self.img_type, ' ]'])


# this represents a collection of images
class Catalog(models.Model):
  name =  models.CharField(max_length=32) #identifier
  description = models.CharField(max_length=300, blank=True) # further description

  def __unicode__(self):
    return ''.join([
      'Catalog [ id: %02i | name: %s | descr: %s ]' % (
         self.pk,
         self.name,
         self.description if self.description else "-----" )])
  
class ModellingResult(models.Model):
  #id = models.AutoField(primary_key=True)
  #basic_data_obj = models.ForeignKey(BasicLensData, blank=True, null=True)
  lens_data_obj = models.ForeignKey(LensData, blank=True, null=True)
  json_str = models.TextField() # the json model string from the frontside UI
  is_final_result = models.BooleanField() # did the user send this model in for storage (true) or was it temprarily saved for a test rendering

  #administrative fields
  created = models.DateTimeField(auto_now_add=True) #when was it added
  created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)# by who was it added
  created_by_str = models.CharField(max_length=200, blank=True)

  rendered_last = models.DateTimeField(blank=True, null=True) #when was it last rendered (then was it started?)
  last_accessed = models.DateTimeField(blank=True, null=True) #when was it last accessed
  is_rendered = models.BooleanField(blank=True) # are the results (images) still available?
  task_id = models.CharField(max_length=100, blank=True)
  local_url = models.CharField(max_length=200, blank=True)
  
  # some data about this simulation that will be kept direcly in the database
  
  # first some general glass settings
  # for the meaning look at a example glass config file, like: glass/Examples/b1115.gls
  n_models = models.IntegerField(blank=True, null=True)
  pixrad = models.IntegerField(blank=True, null=True)
  hubbletime = models.FloatField(blank=True, null=True)
  steepness_min = models.FloatField(blank=True, null=True)
  steepness_max = models.CharField(max_length=200, blank=True)
  smooth_val = models.FloatField(blank=True, null=True)
  smooth_include_central = models.BooleanField(blank=True)
  local_gradient = models.FloatField(blank=True, null=True)
  is_symm = models.BooleanField(blank=True)
  maprad = models.FloatField(blank=True, null=True)
  shear = models.FloatField(blank=True, null=True)
  
  #some glass settings originating from the model  
  redshift_lens = models.FloatField(blank=True, null=True)
  redshift_source = models.FloatField(blank=True, null=True)
  n_sources = models.FloatField(blank=True, null=True) # the number of sources in the image
  n_images = models.IntegerField(blank=True, null=True) # the overal count of images (from all sources)
  
  # some of the results from the simulation
  log_text = models.TextField(blank=True) # the resulting log file contents (from the LAST time this simulation was run)
  


  def __unicode__(self):
    return ''.join(['ModRes [ id: ', `self.pk`,
                    ' | modelId: ' , `self.lens_data_obj.id`,
                    ' | userId: '  , self.created_by_str, #(self.created_by.username if self.created_by is not None else self.created_by_str),
                    ' | @ '        , str(self.created),
                    ' | final: '   , ('X' if self.is_final_result else "_"), " ]"])
  



# a ModelingSession is a intermediate table representing a many to many relationship
# why not use directly the Modellingresult?
# we'll have lazy user access (instead of anonymous)
# if one doen't come back, his entries in this data base will be deleted.
# but the work he has done (saved in the ModellingResult table) will be kept
# (see the created_by key of results with attribute on_delete=models.SET_NULL that prevents
# deletion of this entry even thou the user is deleted. this is NOT prevented here)
class ModellingSession(models.Model):
  user = models.ForeignKey(User)
  basic_data_obj = models.ForeignKey(BasicLensData)
  created = models.DateTimeField(auto_now_add=True) #when was it added
  result = models.ForeignKey('ModellingResult')
  
  
  def __unicode__(self):
    return ''.join(['ModSession [ id:', `self.pk`,
                    ' | user: ', self.user.username,
                    ' | modelID: ', `self.basic_data_obj.pk`,
                    ' | resultID: ', `self.result.pk`,
                    ' | @ ', str(self.created), ' ]' ])
    
    
    
    
    