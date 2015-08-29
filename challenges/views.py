import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View

from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import Challenge
from .forms import ChallengeForm

from main.utils import LoginRequiredMixin
from celery_app.tasks import save_code


class ChallengeList(LoginRequiredMixin, ListView):
    model = Challenge


class ChallengeRun(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'key': 'Value'})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data', {}))
        code = data.get('code')
        if code:
            save_code.delay(code)
            return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': 'NOK'})


class ChallengeAdd(CreateView):
    model = Challenge
    form_class = ChallengeForm
    success_url = '/challenge/list'


class ChallengeDetails(LoginRequiredMixin, DetailView):
    model = Challenge


class ChallengeEdit(LoginRequiredMixin, UpdateView):
    model = Challenge
    form_class = ChallengeForm
