from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings

from braces.views import CsrfExemptMixin, LoginRequiredMixin

from .utils import send_email
from users.models import AppUser
from challenges.models import Challenge
from main.models import Notification

import datetime


class IndexView(TemplateView):
    template_name = 'main/index.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/panel.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        date_from = datetime.datetime.now() + datetime.timedelta(-30)
        new_users = AppUser.objects.filter(
                created_at__gte=date_from).order_by('-created_at')
        latest_challenges = Challenge.objects.order_by('-created_at')[:5]

        context['latest_challenges'] = latest_challenges
        context['new_users'] = new_users
        return context


class FeedbackView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        author = request.user.email
        feedback = request.POST.get('data')
        if feedback:
            message = '{} wrote:\n\n{}'.format(author, feedback)
            send_email(email_address=settings.ADMIN_EMAIL_ADDRESS,
                       body=message, subject='PyWars Feedback')
        return JsonResponse({'ok': True})


class HallOfFame(LoginRequiredMixin, TemplateView):
    template_name = 'main/hall_of_fame.html'

    def get_context_data(self, **kwargs):
        context = super(HallOfFame, self).get_context_data(**kwargs)
        context['top_ten'] = AppUser.objects.filter(
                points__gt=0).order_by('-points', '-created_at')[:10]
        return context


class Notifications(View):

    def post(self, request, *args, **kwargs):
        user = request.user

        action = request.GET.get('action')
        if not action:
            return HttpResponseBadRequest("Missing parameter: 'action'")

        if action == 'dismiss':
            Notification.objects.filter(
                    notified_user=user).update(is_new=False)
        elif action == 'deactivate':
            notification_id = request.GET.get('id')
            if not notification_id:
                return HttpResponseBadRequest("Missing parameter: 'id'")
            Notification.objects.filter(
                    id=notification_id).update(active=False)

        return JsonResponse({'ok': True})

