from django.http import HttpResponse

from django.views.generic.base import View
from django.http import JsonResponse

from main.utils import LoginRequiredMixin
from .tasks import save_code

import json


class RunCode(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hey there!')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data', {}))
        code = data.get('code')
        if code:
            save_code.delay(code)
            return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': 'error'})

