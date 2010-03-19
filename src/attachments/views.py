from django.contrib.auth.decorators import login_required

from forms import AttachmentForm

def ajax_upload(request):
    attachment_form = AttachmentForm(user=request.user)
    if request.method == "POST":
        attachment_form = AttachmentForm(request.POST, request.FILES, user=request.user, \
                actived=False)
        if  attachment_form.is_valid():
            attachment = attachment_form.save()
        return attachment
    return None
change = login_required(ajax_upload)
