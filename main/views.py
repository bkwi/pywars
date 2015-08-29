from django.shortcuts import render
from django.views.generic.base import TemplateView

from main.utils import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = 'main/index.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/panel.html'
