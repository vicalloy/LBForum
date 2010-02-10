from django.shortcuts import render_to_response
from django.template import RequestContext

def profile(request, template_name="account/profile.html"):
    ext_ctx = {}
    return render_to_response(template_name, ext_ctx, RequestContext(request))
