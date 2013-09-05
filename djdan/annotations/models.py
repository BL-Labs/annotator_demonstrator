from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
  creator = models.ForeignKey(User)
  tag = models.CharField(max_length=100)
  
  def __unicode__(self):
    return self.tag

class Item(models.Model):
  TYPES = (
    ('img', 'Image'),
    ('web', 'Webpage'),
    ('txt', 'Text quotation'),
    ('aud', 'Audio file'),
    ('vid', 'YouTube video'),
  )

  creator = models.ForeignKey(User)
  tag = models.CharField(max_length=100, blank=True)
  itemtype = models.CharField(max_length=3,
                              choices=TYPES,
                              default='img')
  payload = models.TextField()
  src = models.TextField(blank=True)
  collection = models.ForeignKey(Collection, related_name="playlist")

  def __unicode__(self):
    if self.tag:
      return self.tag
    elif (self.payload) > 10:
      return self.payload[:10] + "..."
    else:
      return self.payload

# Create your models here.
class AnnotationSession(models.Model):
  creator = models.ForeignKey(User)
  title = models.CharField(max_length=100, blank=True)
  description = models.TextField(blank=True) 
  datestamp = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return self.title

class Annotation(models.Model):
  creator = models.ForeignKey(User)
  leftitem = models.ForeignKey(Item, related_name="left")
  rightitem = models.ForeignKey(Item, related_name="right")
  session = models.ForeignKey(AnnotationSession, related_name="annotations")
  annotation = models.TextField(blank=True)
  datestamp = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    return "%s <-> %s" % (self.leftitem.__unicode__(), self.rightitem.__unicode__())
