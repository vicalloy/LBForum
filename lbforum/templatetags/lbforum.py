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

@register.filter
def post_style(forloop):
    styles = ''
    if forloop['first']:
        styles = 'firstpost topicpost'
    else:
        styles = 'replypost'
    if forloop['last']:
        styles += ' lastpost'
    return styles

@register.filter
def online(user):#TODO... to a common app
    return 'Online'
    if user.lbforum_profile.is_online:
        return 'Online'
    return 'Offline'
