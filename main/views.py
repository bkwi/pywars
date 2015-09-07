from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.http import JsonResponse

from braces.views import CsrfExemptMixin, LoginRequiredMixin


class IndexView(TemplateView):
    template_name = 'main/index.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/panel.html'

