from onlineuser.models import Online

class OnlineUserMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                online = request.user.online
                online.save()
            except:
                pass    
        else:
            ip=request.META['REMOTE_ADDR']
            try:
                Online.get(ident=ip).save();
            except Exception, e:
                Online(ident=ip).save()
