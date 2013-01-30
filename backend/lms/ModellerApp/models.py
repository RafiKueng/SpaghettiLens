from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BasicLensData(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=200)
  
  IMGTYPE_CHOICES = (
    ('BW', 'multi channels, each a grayscale image'),
    ('CO', 'multi channels, one single color image'),
  )
  BAND_CHOICES = (
    ('U', 'UV, 365nm'),
    ('B', 'blue, 445nm'),
    ('V', 'visual, 551nm'),
    ('G', 'green, 551nm'),
    ('R', 'red, 658nm'),
    ('I', 'nearIR, 806nm'),
    ('Z', 'nearIR, 900nm'),
    ('Y', 'nearIR, 1020nm'),
    ('J', 'nearIR, 1220nm'),
    ('H', 'nearIR, 1630nm'),
    ('K', 'nearIR, 2190nm'),
    ('L', 'nearIR, 3450nm'),
    ('M', 'midIR, 4750nm'),
    ('N', 'midIR, ????nm'),
    ('Q', 'midIR, ????nm'),
  )
  
  imgType = models.CharField(max_length=2, choices=IMGTYPE_CHOICES)
  
  channel1_imgurl = models.CharField(max_length=200)
  channel1_type = models.CharField(max_length=1, choices=BAND_CHOICES, blank=True)
  channel1_data = models.CharField(max_length=200, blank=True)
  
  channel2_imgurl = models.CharField(max_length=200, blank=True)
  channel2_type = models.CharField(max_length=1, choices=BAND_CHOICES, blank=True)
  channel2_data = models.CharField(max_length=200, blank=True)

  channel3_imgurl = models.CharField(max_length=200, blank=True)
  channel3_data = models.CharField(max_length=200, blank=True)
  channel3_type = models.CharField(max_length=1, choices=BAND_CHOICES, blank=True)
  
  # who has already modeled this dataset? a many to one relation ship
  modellers = models.ManyToManyField(User, through='ModellingSession')
    
  def __unicode__(self):
    return ''.join([`self.pk`, ' ("', self.name, '" type: ', self.imgType, ')'])



  
class ModellingResult(models.Model):
  #id = models.AutoField(primary_key=True)
  model_id = models.ForeignKey(BasicLensData)
  model_str = models.TextField() # the json model string from the frontside UI
  is_final_result = models.BooleanField() # did the user send this model in for storage (true) or was it temprarily saved for a test rendering

  #administrative fields
  created = models.DateTimeField(auto_now_add=True) #when was it added
  created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)# by who was it added
  rendered_last = models.DateTimeField(blank=True) #when was it last rendered
  is_rendered = models.BooleanField(blank=True) # are the results (images) still available?
  
  # some data about this simulation that will be kept direcly in the database
  
  # first some general glass settings
  # for the meaning look at a example glass config file, like: glass/Examples/b1115.gls
  n_models = models.IntegerField(blank=True)
  pixrad = models.IntegerField(blank=True)
  steepness_min = models.FloatField(blank=True)
  steepness_max = models.FloatField(blank=True)
  smooth_val = models.FloatField(blank=True)
  smooth_include_central = models.BooleanField(blank=True)
  local_gradient = models.FloatField(blank=True)
  is_symm = models.BooleanField(blank=True)
  maprad = models.FloatField(blank=True)
  shear = models.FloatField(blank=True)
  
  #some glass settings originating from the model  
  redshift_lens = models.FloatField(blank=True)
  redshift_source = models.FloatField(blank=True)
  n_sources = models.FloatField(blank=True) # the number of sources in the image
  n_images = models.IntegerField(blank=True) # the overal count of images (from all sources)
  
  # some of the results from the simulation
  log_text = models.TextField(blank=True) # the resulting log file contents (from the LAST time this simulation was run)
  


  def __unicode__(self):
    return ''.join(['res: ', `self.pk`, ' (modelid: ',
                    `self.model.id`, ' @', str(self.dateTime),
                    " final:", ('X' if self.isFinalResult else "_"), ")"])
  



# a ModelingSession is a intermediate table representing a many to many relationship
# why not use directly the Modellingresult?
# we'll have lazy user access (instead of anonymous)
# if one doen't come back, his entries in this data base will be deleted.
# but the work he has done (saved in the ModellingResult table) will be kept
# (see the created_by key of results with attribute on_delete=models.SET_NULL that prevents
# deletion of this entry even thou the user is deleted. this is NOT prevented here)
class ModellingSession(models.Model):
  user = models.ForeignKey(User)
  lens_data = models.ForeignKey(BasicLensData)
  created = models.DateTimeField(auto_now_add=True) #when was it added
  result = models.ForeignKey('ModellingResult')