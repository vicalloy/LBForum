from django import template

register = template.Library()

@register.filter
def topic_icon(topic): 
    if topic.closed:
        return 'closed'
    elif topic.sticky:
        return 'sticky'
    else:
        return 'normal'
