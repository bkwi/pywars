from django.views.generic import ListView, CreateView, UpdateView, View
from django.views.generic.edit import FormView
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse

from .models import Challenge, Solution, Vote, SolutionComment
from .forms import ChallengeForm, SolutionForm
from main.utils import logger

from braces.views import LoginRequiredMixin

import pickle
import base64
import json


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

        challenge = Challenge.objects.get(pk=self.kwargs.get('pk'))
        tests = challenge.tests_as_list_of_strings()

        context['challenge'] = challenge
        context['tests'] = base64.encodestring(pickle.dumps(tests))
        context['websocket_url'] = settings.WEBSOCKET_URL

        return context

    def form_valid(self, form):
        solution = form.save(commit=False)
        challenge_solved = Challenge.objects.get(pk=solution.challenge_id)
        user = self.request.user
        if not user.already_solved_challenge(challenge_solved):
            user.points += challenge_solved.points
            user.save()
        solution.save()
        logger.info('%s solved challenge %s. Solution id: %s',
                    user, challenge_solved.id, solution.id)
        return redirect(self.success_url)


class ChallengeEdit(LoginRequiredMixin, UpdateView):
    model = Challenge
    form_class = ChallengeForm


class ChallengeSolutions(LoginRequiredMixin, ListView):
    model = Solution
    template_name = 'challenges/challenge_solutions_list.html'

    def get_context_data(self, **kwargs):
        challenge = Challenge.objects.get(id=self.kwargs.get('pk'))
        solutions = []

        if self.request.user.already_solved_challenge(challenge):
            solutions = Solution.objects.filter(
                    challenge_id=challenge.id).order_by('-votes_count').select_related()

        return {'solutions': solutions }


class VoteOnSolution(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        solution = Solution.objects.get(id=self.kwargs.get('pk'))
        if Vote.objects.filter(solution=solution, user=request.user):
            return JsonResponse({'ok': False})

        vote = Vote(solution=solution, user=request.user)
        vote.save()

        solution.votes_count += 1
        solution.save()
        logger.info('%s voted on solution %s', request.user, solution.id)
        return JsonResponse({'ok': True, 'new_value': solution.votes_count})


class SolutionCommentAPI(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        data = json.loads(request.GET.get('data', {}))
        solution_id = data.get('solutionId')
        solution = Solution.objects.get(id=solution_id)
        comments_list = solution.comments_list()

        return JsonResponse({'ok': True,
                             'comments': comments_list})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data', {}))
        comment_body = data.get('body')
        solution_id = data.get('solutionId')
        if not solution_id and user_id:
            return JsonResponse({'ok': False})

        solution = Solution.objects.get(id=solution_id)
        comment = SolutionComment(solution=solution,
                                  author=request.user,
                                  body=comment_body)
        comment.save()
        data = {'commentId': comment.id,
                'author': comment.author.name,
                'createdAt': comment.created_at.__str__()[:16],
                'avatarUrl': comment.author.avatar_url(),
                'body': comment.body}

        logger.info('%s added a comment to solution %s. Comment id: %s',
                    request.user, solution_id, comment.id)

        # data should be returned as one-element list
        return JsonResponse({'ok': True, 'comments': [data]})

