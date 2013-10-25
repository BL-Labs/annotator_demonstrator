from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
  TYPES = (
    ('img', 'Image'),
    ('web', 'Webpage'),
    ('txt', 'Text quotation'),
    ('aud', 'Audio file'),
    ('vid', 'YouTube video'),
  )
  created = models.DateTimeField(auto_now_add=True)
  creator = models.ForeignKey(User)
  tag = models.CharField(max_length=100, blank=True)
  itemtype = models.CharField(max_length=3,
                              choices=TYPES,
                              default='img')
  payload = models.TextField()
  src = models.TextField(blank=True)

  def __unicode__(self):
    if self.tag:
      return self.tag
    elif (self.payload) > 10:
      return self.payload[:10] + "..."
    else:
      return self.payload

class Collection(models.Model):
  creator = models.ForeignKey(User)
  created = models.DateTimeField(auto_now_add=True)
  tag = models.CharField(max_length=100)
  location = models.IntegerField()
  playlist = models.ManyToManyField(Item, through='CollectionEntry')

  def __unicode__(self):
    return self.tag

class CollectionEntry(models.Model):
  collection = models.ForeignKey(Collection)
  item = models.ForeignKey(Item)
  position = models.IntegerField()
  shortlabel = models.CharField(max_length="50", blank=True)
  
  def __unicode__(self):
    if self.shortlabel:
      return self.shortlabel
    else:
      return u"Item: {0} at position {1} in collection {2}".format(unicode(self.item), unicode(self.position), unicode(self.collection))

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
  leftitem_state = models.CharField(max_length=30, blank=True)
  rightitem_state = models.CharField(max_length=30, blank=True)
  datestamp = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    if self.annotation:
      return "%s <- ** -> %s" % (self.leftitem.__unicode__(), self.rightitem.__unicode__())
    else:
      return "%s <-    -> %s" % (self.leftitem.__unicode__(), self.rightitem.__unicode__())
 
