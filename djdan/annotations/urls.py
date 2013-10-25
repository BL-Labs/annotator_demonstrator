from django.conf.urls import patterns, url

from annotations import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^session$', views.sessionlist, name='sessionlist'),
    url(r'^session/(?P<session_id>\d+)$', views.session, name='session'),
    url(r'^annotations$', views.annotationlist, name='annotationlist'),
    url(r'^annotations/(?P<annotation_id>\d+)$', views.annotation, name='annotation'),
    url(r'^collections$', views.collectionlist, name='collectionlist'),
    url(r'^collections/(?P<collection_id>\d+)$', views.collection, name='collections'),
    url(r'^items$', views.itemlist, name='itemlist'), 
    url(r'^items/(?P<item_id>\d+)$', views.item, name='item'), 
    url(r'^login$', views.login_view, name='loginview'),
    url(r'^logout$', views.logout_view, name='logout'),
)
