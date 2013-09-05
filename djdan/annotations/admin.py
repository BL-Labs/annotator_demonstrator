from django.contrib import admin
from annotations.models import Annotation, AnnotationSession, Collection, Item

admin.site.register(Annotation)
admin.site.register(AnnotationSession)
admin.site.register(Collection)
admin.site.register(Item)
