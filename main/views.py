from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.http import JsonResponse

from braces.views import CsrfExemptMixin, LoginRequiredMixin

from main.utils import push


class IndexView(TemplateView):
    template_name = 'main/index.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/panel.html'


class PusherAuth(CsrfExemptMixin, View):

    def post(self, request, *args, **kwargs):
        auth = push.authenticate(
            channel=request.POST.get('channel_name'),
            socket_id=request.POST.get('socket_id'))
        return JsonResponse(auth)

