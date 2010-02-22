from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User

def profile(request, user_id=None, template_name="account/profile.html"):
    view_user = request.user
    if user_id:
        view_user = get_object_or_404(User, pk = user_id)
    view_only = view_user != request.user
    ext_ctx = {'view_user':view_user, 'view_only':view_only }
    return render_to_response(template_name, ext_ctx, RequestContext(request))
