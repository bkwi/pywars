import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View, TemplateView

from main.utils import LoginRequiredMixin
from celery_app.tasks import save_code


class Challenge(TemplateView): # how about detail view?
    template_name = 'challenges/challenge.html'


class ChallengeRun(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'key': 'Value'})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data', {}))
        code = data.get('code')
        if code:
            save_code.delay(code)
            return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': 'NOK'})
