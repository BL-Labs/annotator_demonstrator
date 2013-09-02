from django.db import models

# Create your models here.
class AnnotationSession(models.Model):
  startedby = models.CharField(max_length=30)
  description = models.TextField() 
  datestamp = models.DateTimeField(auto_now_add=True)

class Annotation(models.Model):
  author = models.CharField(max_length=30)
  leftitem = models.CharField(max_length=255)
  rightitem = models.CharField(max_length=255)
  session = models.ForeignKey(AnnotationSession)
  annotation = models.TextField()
  datestamp = models.DateTimeField(auto_now_add=True)

