from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.conf import settings

from .models import Challenge
from .forms import ChallengeForm

from braces.views import LoginRequiredMixin


class ChallengeList(LoginRequiredMixin, ListView):
    model = Challenge


class ChallengeAdd(CreateView):
    model = Challenge
    form_class = ChallengeForm
    success_url = '/challenge/list'


class ChallengeDetails(LoginRequiredMixin, DetailView):
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super(ChallengeDetails, self).get_context_data(**kwargs)
        ch_name = settings.PUSHER_CHANNEL.format(self.request.user.id)
        context['channel_name'] = ch_name
        return context


class ChallengeEdit(LoginRequiredMixin, UpdateView):
    model = Challenge
    form_class = ChallengeForm
