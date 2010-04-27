#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

def json_response(data):
    return HttpResponse(simplejson.dumps(data), mimetype='text/html')#application/json

def _ajax_login_required(msg):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return json_response({'valid': False, 'msg': msg})
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def ajax_login_required(function=None, msg=_('please login first')):
    actual_decorator = _ajax_login_required(msg)
    if function:
        return actual_decorator(function)
    return actual_decorator

def request_get_next(request):
    """
    The part that's the least straightforward about views in this module is how they 
    determine their redirects after they have finished computation.

    In short, they will try and determine the next place to go in the following order:

    1. If there is a variable named ``next`` in the *POST* parameters, the view will
    redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters, the view will
    redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers, the view will
    redirect to that previous page.
    """
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    if not next:
        next = request.path
    return next
