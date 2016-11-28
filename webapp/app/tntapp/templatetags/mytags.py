from django import template
import json
import itertools

register = template.Library()

@register.filter
def decodejson(data):
    return json.loads(data)

@register.filter
def encode2json(data):
    return json.dumps(data)
