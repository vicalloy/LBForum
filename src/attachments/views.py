import django.dispatch
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.csrf.middleware import csrf_exempt
from django.http import HttpResponse

from djangohelper.helper import flash_login_required, ajax_login_required, \
        json_response

from forms import AttachmentForm
from models import Attachment

@csrf_exempt
@flash_login_required
def __ajax_upload(request):
    data = {'valid': False, 'errors': ugettext('no file')}
    attachment_form = AttachmentForm(user=request.user)
    if request.method == "POST":
        attachment_form = AttachmentForm(request.POST, request.FILES, user=request.user, \
                actived=False)
        #TODO improve validate
        if  attachment_form.is_valid():
            attachment = attachment_form.save()
            data['valid'] = True
            data.pop('errors')
            data['attachment'] = {'id': attachment.id, \
                    'fn': attachment.org_filename, 'url': attachment.file.url, 'descn': ''}
        else:
            #attachment_form.errors
            pass
    return json_response(data)

ajax_upload = csrf_exempt(ajax_login_required(__ajax_upload))
uploadify = csrf_exempt(flash_login_required(__ajax_upload))

@csrf_exempt
@ajax_login_required
def ajax_delete(request):
    data = {'valid': False, 'errors': ugettext('some errors...')}
    attachment_id = request.POST['id']
    attachment = Attachment.objects.get(pk=attachment_id)
    if (attachment.user != request.user):
        data['errors'] = ugettext('no right')
    else:
        attachment.delete()
        data['valid'] = True
        data.pop('errors')
    return json_response(data)

@csrf_exempt
@ajax_login_required
def ajax_change_descn(request):
    #TODO AJAX POST ONLY
    #TODO HANDEL AJAX ERROR
    data = {'valid': False, 'errors': ugettext('some errors...')}
    attachment_id = request.POST['id']
    attachment = Attachment.objects.get(pk=attachment_id)
    if (attachment.user != request.user):
        data['errors'] = ugettext('no right')
    elif request.method == "POST":
        attachment.description = request.POST['descn']
        data['valid'] = True
        data.pop('errors')
        attachment.save()
    return json_response(data)

upload_recieved = django.dispatch.Signal(providing_args=['data'])
