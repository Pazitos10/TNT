import json

from django import template

register = template.Library()

@register.filter
def decodejson(data):
    return json.loads(data)

@register.filter
def encode2json(data):
    return json.dumps(data)
