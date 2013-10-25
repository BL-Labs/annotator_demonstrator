from django.contrib import admin
from annotations.models import Annotation, AnnotationSession, Collection, Item, CollectionEntry

admin.site.register(Annotation)
admin.site.register(AnnotationSession)
admin.site.register(CollectionEntry)
admin.site.register(Collection)
admin.site.register(Item)
