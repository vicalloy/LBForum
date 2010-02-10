from onlineuser.models import Online

class OnlineUserMiddleware:
    def process_request(self, request):
        user = request.user
        if user.is_authenticated():
            o, created = Online.objects.get_or_create(user=user)
        else:
            ip=request.META['REMOTE_ADDR']
            o, created = Online.objects.get_or_create(ident=ip)
        if not created:
            o.save()
