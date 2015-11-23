from django.conf import settings

def common_context(request):
    cc = {'websocket_url': settings.WEBSOCKET_URL}
    user = request.user
    if user.is_authenticated():
        cc['notifications'] = user.notifications.all()[:10]
    return cc
