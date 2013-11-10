# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader

from django.shortcuts import redirect

from django.db.models import Max

from annotations.models import Annotation, AnnotationSession, Collection, Item, CollectionEntry

from django.contrib.auth import authenticate, login, logout

import json

def login_view(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    next = request.POST['next']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        # Redirect to a success page.
        return redirect("collectionlist")
      else:
        # Return a 'disabled account' error message
        template = loader.get_template("annotations/login.html")
        return HttpResponse(template.render(RequestContext(request, {'message':'Account disabled'})))
    else:
      # Return an 'invalid login' error message.
      if next:
        redirect(next)
      template = loader.get_template("annotations/login.html")
      return HttpResponse(template.render(RequestContext(request, {'message':'Invalid login'})))
  else:
    template = loader.get_template("annotations/login.html")
    return HttpResponse(template.render(RequestContext(request, {})))

def logout_view(request):
  logout(request)
  return redirect("loginview")  

def index(request):
  template = loader.get_template("annotations/index.html")
  context = RequestContext(request, {})
  return HttpResponse(template.render(context))

def sessionlist(request):
  if request.method == "GET":
    template = loader.get_template("annotations/sessionlist.html")
    session_list = AnnotationSession.objects.all()
    context = RequestContext(request, {
      'session_list': session_list,
    })
    return HttpResponse(template.render(context))
  elif request.method == "POST":
    if not request.user.is_authenticated():
      return redirect('login')
    title = request.POST['title']
    description = request.POST['description']
    newsession = AnnotationSession.objects.create(creator=request.user, title=title, description=description)
    return redirect('session', session_id=newsession.id)
    

def session(request, session_id):
  try:
    annotationsession = AnnotationSession.objects.get(pk=session_id)
    session_annotations = annotationsession.annotations.all()
  except AnnotationSession.DoesNotExist:
    return HttpResponse(status=404)
  if request.method == "GET":
    template = loader.get_template("annotations/session.html")
    context = RequestContext(request, {
      'session': annotationsession,
      'annotations': session_annotations,
    })
    return HttpResponse(template.render(context))
  elif request.method == "POST":
    if not request.user.is_authenticated():
      return redirect('login')
    leftitem = request.POST['leftitem']
    rightitem = request.POST['rightitem']
    annotation = request.POST['annotation']
    try:
      leftitemobj = Item.objects.get(pk=int(leftitem))
      rightitemobj = Item.objects.get(pk=int(rightitem))
      prevannotation = annotationsession.annotations.filter(leftitem=leftitemobj, rightitem=rightitemobj)
      if prevannotation and len(prevannotation)==1:
        prevannotation.annotation = annotation
        # add state saving
        prevannotation.save()
        return redirect('annotation', annotation_id=prevannotation.id)
    except Annotation.NotFound:
      leftitemobj = Item.objects.get(pk=int(leftitem))
      rightitemobj = Item.objects.get(pk=int(rightitem))
      newannotation = Annotation.objects.create(leftitem=leftitemobj, rightitem=rightitemobj, creator=request.user, annotation=annotation, session=annotationsession)
      return redirect('annotation', annotation_id=newannotation.id)
  elif request.method == "DELETE":
    if not request.user.is_authenticated():
      return redirect('login')
    annotationsession.delete()
    return HttpResponse("", status=204)

def item_snippet(request, item_id):
  try:
    item = Item.objects.get(pk=item_id)
  except Item.DoesNotExist:
    return HttpResponse(status=404)
  template = loader.get_template("annotations/item.html")
  context = RequestContext( request, {'item': item})
  return HttpResponse(template.render(context))
  
def collection(request, collection_id):
  try:
    col = Collection.objects.get(pk=collection_id)
  except Collection.DoesNotExist:
    return HttpResponse(status=404)
  template = loader.get_template("annotations/collection.html")
  items = CollectionEntry.objects.filter(collection=col)
  unassigned = Item.objects.filter(creator=request.user)
  if request.method == "GET":
    context = RequestContext( request, {
        'collection': col,
        'col': col,
        'items': items,
        'unassigned': unassigned,
              })
    return HttpResponse(template.render(context))
  if request.method == "POST":
    if not request.user.is_authenticated():
      return redirect('login')
    # add new item
    unassigned_flag = request.POST['unassigned']
    tag = request.POST['tag']
    if unassigned_flag != "no":
      itemid = request.POST['unassigneditem']
      newitem = Item.objects.get(pk=itemid)
      thisstatus = 200
      if not newitem:
        return HttpResponse(status=400)
    else:
      tag = request.POST['tag']
      payload = request.POST['payload']
      itemtype = request.POST['itemtype']
      src = request.POST['src']
      newitem = Item.objects.create(creator=request.user, payload=payload, itemtype=itemtype, src=src, tag=tag)
      thisstatus = 201
    maxpos = CollectionEntry.objects.filter(collection=col).aggregate(Max('position'))
    position = maxpos['position__max']
    if not position:
      position = 0
    ce = CollectionEntry(collection=col, item=newitem, position=position, shortlabel=tag)
    ce.save()
    return redirect('collections', collection_id = col.id)

def collectionlist(request):
  if not request.user.is_authenticated():
    return redirect('login')
  collections = Collection.objects.filter(creator=request.user).all()
  items = Item.objects.filter(creator=request.user).exclude(collection__isnull=True)
  if request.method == "GET":
    template = loader.get_template("annotations/collectionlist.html")
    context = RequestContext( request, {
        'collections': collections,
        'unassigned': items,
              })
    return HttpResponse(template.render(context))
  elif request.method == "POST":
    tag = request.POST['tag']
    location = request.POST['location']
    col = Collection.objects.create(tag=tag, location=location, creator=request.user)
    return redirect('collections', collection_id=col.id)

def itemlist(request):
  if not request.user.is_authenticated():
    return redirect('login')
  items = Item.objects.filter(creator=request.user)
  collections = Collection.objects.filter(creator=request.user)
  if request.method == "GET":
    template = loader.get_template("annotations/itemlist.html")
    context = RequestContext( request, {
        'items': items,
        'collections': collections,
              })
    return HttpResponse(template.render(context))
  if request.method == "POST":
    if not request.user.is_authenticated():
      return redirect('login')
    tag = request.POST.get('tag',"")
    payload = request.POST.get('payload',"")
    itemtype = request.POST.get('itemtype',"img")
    src = request.POST.get('src',"")
    newitem = Item.objects.create(tag = tag, 
                      itemtype=itemtype,
                      payload=payload,
                      src=src)
    newitem.save()
    return redirect("item", item_id=updateitem.id)

def item(request, item_id):
  try:
    item = Item.objects.get(pk=item_id)
  except Item.DoesNotExist:
    return HttpResponse(status=404)
  if request.method == "GET":
    template = loader.get_template("annotations/itemview.html")
    allcollections = Collection.objects.filter(creator=request.user)
    context = RequestContext( request, {
        'allcollections': allcollections,
        'item': item,
              })
    return HttpResponse(template.render(context))
  if request.method == "POST":
    if not request.user.is_authenticated():
      return redirect('login')
    itemid = request.POST['itemid']
    tag = request.POST['tag']
    payload = request.POST['payload']
    itemtype = request.POST['itemtype']
    src = request.POST['src']
    updateitem = Item.objects.get(pk=int(itemid))
    updateitem.tag = tag
    updateitem.itemtype = itemtype
    updateitem.payload = payload
    updateitem.src = src
    updateitem.save()
    return redirect("item", item_id=updateitem.id)


def annotation(request, session_id):
  # GET => gather collections and render UI
  # POST => get annotation information and create new/update annotation.
  if not request.user.is_authenticated():
    return redirect('login')
  collections = Collection.objects.filter(creator=request.user).all()
  try:
    annotationsession = AnnotationSession.objects.get(pk=session_id)
    session_annotations = annotationsession.annotations.all().order_by("datestamp")
  except AnnotationSession.DoesNotExist:
    return HttpResponse(status=404)

  if request.method == "GET":
    context = RequestContext( request, {'collections': collections,
                                        'annotationsession': annotationsession,
                                        'annotations': session_annotations })
    template = loader.get_template("annotations/annotate.html")
    return HttpResponse(template.render(context))
  elif request.method == "POST":
    # A new annotation or an old one?
    leftitem_id = request.POST.get("leftitem")
    rightitem_id = request.POST.get("rightitem")
    try:
      leftitem = Item.objects.get(pk=leftitem_id)
      rightitem = Item.objects.get(pk=rightitem_id)
    except Item.DoesNotExist:
      print("Hmmm it says these don't exist")
      return HttpResponse(status=404)
      
    leftitem_state = request.POST.get("leftitem_state")
    rightitem_state = request.POST.get("rightitem_state")
    annotationtext = request.POST.get("annotationtext", u"")
    
    try:
      previous = Annotation.objects.get(leftitem = leftitem, rightitem = rightitem, session = annotationsession)
      previous.annotation = annotationtext
      previous.leftitem_state = leftitem_state
      previous.rightitem_state = rightitem_state
      previous.save()
      return HttpResponse("{{'annotation_id':'{0}'}}".format(str(previous.id)), mimetype="application/json")
    except Annotation.DoesNotExist:
      new_anno = Annotation(leftitem = leftitem, 
                          rightitem = rightitem, 
                          session = annotationsession,
                          leftitem_state = leftitem_state,
                          rightitem_state = rightitem_state,
                          creator = request.user)
      new_anno.save()
      return HttpResponse("{{'annotation_id':'{0}'}}".format(str(new_anno.id)), mimetype="application/json")

def annotation_query(request, session_id, leftitem_id, rightitem_id):
  try:
    annotationsession = AnnotationSession.objects.get(pk=session_id)
    leftitem = Item.objects.get(pk=leftitem_id)
    rightitem = Item.objects.get(pk=rightitem_id)
    anno = Annotation.objects.get(leftitem = leftitem, rightitem = rightitem, session = annotationsession)
    annotation_packet = { 'annotation_id': anno.id,
                   'leftitem': leftitem.id,
                   'rightitem': rightitem_id,
                   'annotation': anno.annotation,
#                   'datestamp': anno.datestamp,
                   'session_id': session_id,
                   'leftitem_state': anno.leftitem_state,
                   'rightitem_state': anno.rightitem_state,
                  }
    data = json.dumps(annotation_packet)
    return HttpResponse(data, mimetype="application/json")
  except AnnotationSession.DoesNotExist:
    # No such session
    return HttpResponse("{}", mimetype="application/json")
  except Annotation.DoesNotExist:
    # No such annotation in this session 
    return HttpResponse("{}", mimetype="application/json")
  except Item.DoesNotExist:
    # No such item
    return HttpResponse("{}", mimetype="application/json")
  
def annotationlist(request):
  pass
