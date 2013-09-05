# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader

from annotations.models import Annotation, AnnotationSession

def index(request):
  template = loader.get_template("annotations/index.html")
  context = RequestContext(request, {})
  return HttpResponse(template.render(context))

def sessionlist(request):
  template = loader.get_template("annotations/sessionlist.html")
  session_list = AnnotationSession.objects.all()
  context = RequestContext(request, {
    'session_list': session_list,
  })
  return HttpResponse(template.render(context))

def session(request, session_id):
  template = loader.get_template("annotations/session.html")
  try:
    annotationsession = AnnotationSession.objects.get(pk=session_id)
    session_annotations = annotationsession.annotations.all()
  except AnnotationSession.DoesNotExist:
    raise Http404
  context = RequestContext(request, {
    'session': annotationsession,
    'annotations': session_annotations,
  })
  return HttpResponse(template.render(context))

def annotationlist(request):
  pass

def annotation(request, annotation_id):
  pass
