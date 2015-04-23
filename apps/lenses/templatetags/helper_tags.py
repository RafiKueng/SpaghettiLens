 
from django import template

register = template.Library()

@register.filter
def getArg(obj, arg):
    return obj['_'+arg]
    
@register.filter
def getID(obj):
    return obj['_id']