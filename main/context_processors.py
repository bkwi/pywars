from django.conf import settings

def common_context(request):
    cc = {'websocket_url': settings.WEBSOCKET_URL}
    user = request.user
    if user.is_authenticated():
        notifications = user.notifications.all()
        cc['notifications'] = notifications[:10]
        cc['new_notifications_count'] = sum([x.is_new for x in notifications])
    return cc
