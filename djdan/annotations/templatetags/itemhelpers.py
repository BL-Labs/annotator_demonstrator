from django import template

register = template.Library()

class ImgNode(template.Node):
  def __init__(self, payload):
    self.img_url = payload

  def render(self, context):
    pagecontext = context.get['pagecontext', 'default']

    return """
<div class="%s">
<img class="annotationimage %s" src="%s" />
</div>""" % (pagecontext, pagecontext, self.img_url)

def represent_item(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        _, itemtype, payload, pagecontext = token.split_contents()
    except ValueError:
        msg = '%r tag requires 3 arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    if itemtype == "img":
      return ItemNode(payload, pagecontext)
