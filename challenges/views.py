from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import Challenge
from .forms import ChallengeForm

from main.utils import LoginRequiredMixin


class ChallengeList(LoginRequiredMixin, ListView):
    model = Challenge


class ChallengeAdd(CreateView):
    model = Challenge
    form_class = ChallengeForm
    success_url = '/challenge/list'


class ChallengeDetails(LoginRequiredMixin, DetailView):
    model = Challenge


class ChallengeEdit(LoginRequiredMixin, UpdateView):
    model = Challenge
    form_class = ChallengeForm
