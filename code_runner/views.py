from django.http import HttpResponse

from django.views.generic.base import View
from django.http import JsonResponse

from challenges.models import Challenge
from main.utils import LoginRequiredMixin
from .tasks import run
from .utils import code_template

import json
from string import Template


class RunCode(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hey there!')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data', {}))

        print "DATA RECEIVED", data

        solution = data.get('solution')
        challenge_id = data.get('challengeId')
        user_id = data.get('userId')
        challenge = Challenge.objects.get(id=challenge_id)

        code = Template(code_template)
        code = code.substitute(solution=solution,
                        test_statements=challenge.tests_as_list_of_strings())

        if solution:
            run(code, challenge_id, user_id)
            return JsonResponse({'status': True, 'msg': 'task queued'})

        return JsonResponse({'status': False, 'msg': 'error'})

