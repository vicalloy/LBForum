from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from postmarkup import create, QuoteTag, PostMarkup

register = template.Library()

#bbcode
class LBQuoteTag(QuoteTag):

    def render_open(self, parser, node_index):
        if self.params:
            return u'<div class="quotebox"><cite>%s:</cite><blockquote><p>'%(PostMarkup.standard_replace(self.params))
        else:
            return u'<div class="quotebox"><blockquote><p>'


    def render_close(self, parser, node_index):
        return u"</p></blockquote></div>"

_postmarkup = create(use_pygments=False, annotate_links=False)
_postmarkup.tag_factory.add_tag(LBQuoteTag, 'quote')

@register.filter
def bbcode(s):
    return _postmarkup(s)
#bbcode end

@register.filter
def form_all_error(form):
    errors = []
    global_error = form.errors.get('__all__', '')
    if global_error:
        global_error = global_error.as_text()
    for name, field in form.fields.items():
        e = form.errors.get(name, '')
        if e:
            errors.append((field.label, force_unicode(e), ))
    return mark_safe(u'<ul class="errorlist">%s %s</ul>'
            % (global_error, ''.join([u'<li>%s%s</li>' % (k, v) for k, v in errors])))

@register.filter
def topic_state(topic): 
    c = []
    if topic.closed:
        c.append('closed')
    elif topic.sticky:
        c.append('sticky')
    else:
        c.append('normal')
    return ' '.join(c)

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
def online(user):
    try:
        if user.online.online():
            return _('Online')
    except Exception, e:
        pass
    return _('Offline')

@register.simple_tag
def page_item_idx(page_obj, forloop):
    return page_obj.start_index() + forloop['counter0']

@register.simple_tag
def page_range_info(page_obj):
    paginator = page_obj.paginator
    if paginator.num_pages == 1:
        return paginator.count
    return str(page_obj.start_index()) +' ' + 'to' + ' ' +  \
            str(page_obj.end_index()) + ' ' + 'of' + ' ' +  str(page_obj.paginator.count)
