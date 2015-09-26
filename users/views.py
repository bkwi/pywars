from django.views.generic import FormView, View, CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import AppUser
from .forms import RegisterUserForm
from main.utils import send_email


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/main/dashboard')
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(
                self.request.GET.get('next', '/main/dashboard'))


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/main')


class RegisterUserView(CreateView):
    model = AppUser
    form_class  = RegisterUserForm
    success_url = '/main'

    def form_valid(self, form):
        send_email(email_address=settings.ADMIN_EMAIL_ADDRESS,
                   body=str(form), subject='PyWars - New user')
        return super(RegisterUserView, self).form_valid(form)

