from django.conf.urls import patterns, url

from annotations import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^session$', views.sessionlist, name='sessionlist'),
    url(r'^session/(?P<session_id>\d+)$', views.session, name='session'),
    url(r'^annotation$', views.annotationlist, name='annotationlist'),
    url(r'^annotation/(?P<annotation_id>\d+)$', views.annotation, name='annotation'),
)
