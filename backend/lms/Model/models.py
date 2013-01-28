from django.db import models

# Create your models here.
class ModelData(models.Model):
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
    
  def __unicode__(self):
    return ''.join([`self.pk`, ' ("', self.name, '" type: ', self.imgType, ')'])

  
class Result(models.Model):
  #id = models.AutoField(primary_key=True)
  model = models.ForeignKey(ModelData)
  dateTime = models.DateTimeField(auto_now_add=True)
  string = models.TextField()
  data = models.ForeignKey('ResultData', blank=True, null=True)
  isFinalResult = models.BooleanField()

  def __unicode__(self):
    return ''.join(['res: ', `self.pk`, ' (modelid: ',
                    `self.model.id`, ' @', str(self.dateTime),
                    " final:", ('X' if self.isFinalResult else "_"), ")"])
  
  
class ResultData(models.Model):
  #id = models.AutoField(primary_key=True);
  data1 = models.CharField(max_length=200)