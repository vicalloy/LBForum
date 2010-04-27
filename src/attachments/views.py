from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.csrf.middleware import csrf_exempt

from djangohelper.helper import ajax_login_required, json_response

from forms import AttachmentForm

@csrf_exempt
@ajax_login_required
def ajax_upload(request):
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
            data['attachment'] = {'id': attachment.id}
        else:
            print attachment_form.errors
    return json_response(data)

@csrf_exempt
@ajax_login_required
def ajax_delete(request, id):
    data = {'valid': False, 'errors': ugettext('')}
    attachment = Attachment.objects.get(pk=id)
    if (attachment.user != request.user):
        data[errors] = 'no right'
    else:
        attachment.delete()
        data['valid'] = True
        data.pop('errors')
    return json_response(data)

@csrf_exempt
@ajax_login_required
def ajax_change_descn(request, id):
    #TODO HANDEL AJAX ERROR
    data = {'valid': False, 'errors': ugettext('')}
    attachment = Attachment.objects.get(pk=id)
    if (attachment.user != request.user):
        data[errors] = 'no right'
    elif request.method == "POST":
        attachment.descn = request.POST['descn']
        data['valid'] = True
        data.pop('errors')
        attachment.save()
    return json_response(data)
