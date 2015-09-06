from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.shortcuts import redirect

from .models import Challenge, Solution
from .forms import ChallengeForm, SolutionForm

from braces.views import LoginRequiredMixin


class ChallengeList(LoginRequiredMixin, ListView):
    model = Challenge


class ChallengeAdd(LoginRequiredMixin, CreateView):
    model = Challenge
    form_class = ChallengeForm
    success_url = '/challenge/list'

class ChallengeSolve(LoginRequiredMixin, FormView):
    template_name = 'challenges/challenge_solve.html'
    form_class = SolutionForm
    success_url = '/main/dashboard/'

    def get_initial(self):
        return {
                    'author': self.request.user,
                    'challenge_id': self.kwargs.get('pk')
                }

    def get_context_data(self, **kwargs):
        context = super(ChallengeSolve, self).get_context_data(**kwargs)

        channel_name = settings.PUSHER_CHANNEL.format(self.request.user.id)
        challenge = Challenge.objects.get(pk=self.kwargs.get('pk'))

        context['challenge'] = challenge
        context['channel_name'] = channel_name

        return context

    def form_valid(self, form):
        solution = form.save(commit=False)
        challenge_solved = Challenge.objects.get(pk=solution.challenge_id)
        user = self.request.user
        if not user.already_solved_challenge(challenge_solved):
            user.points += challenge_solved.points
            user.save()
        solution.save()
        return redirect(self.success_url)


class ChallengeEdit(LoginRequiredMixin, UpdateView):
    model = Challenge
    form_class = ChallengeForm

