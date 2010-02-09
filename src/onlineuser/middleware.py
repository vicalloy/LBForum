from onlineuser.models import Online

class OnlineUserMiddleware:
    def process_request(self, request):
        user = request.user
        if user.is_authenticated():
            try:
                online = user.online
                online.save()
            except Exception, e:
                Online(user=user).save();
        else:
            ip=request.META['REMOTE_ADDR']
            try:
                Online.objects.get(ident=ip).save();
            except Exception, e:
                Online(ident=ip).save()
