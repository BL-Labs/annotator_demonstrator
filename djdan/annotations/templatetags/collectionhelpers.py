from django import template

register = template.Library()

@register.filter
def youtube_helper(youtubeurl):
    id = youtubeurl.split("?v=",1)[-1].split("&")[0]
    return id

@register.filter
def position_style_collection(value_raw):
    value = int(value_raw)
    height = 30 * (value / 15)
    width = 40 * (value % 15)
    return "left: {0}px; bottom: {1}px".format(width, height)


@register.filter
def position_stick(loop_counter):
    value = int(loop_counter)
    return "bottom: {0}px;".format(value * 30)

@register.filter
def position_blob(loop_counter):
    value = int(loop_counter)
    return "bottom: {0}px;".format((value * 30) + 26)
