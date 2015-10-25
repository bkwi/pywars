from django.views.generic import (FormView, View, CreateView, UpdateView,
                                  TemplateView)
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       SetPasswordForm)
from django.contrib.auth import (login, logout, authenticate,
                                 update_session_auth_hash)
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.shortcuts import redirect, render

from braces.views import LoginRequiredMixin

from .models import AppUser
from .forms import RegisterUserForm, UserSettingsForm
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
    success_url = '/main/dashboard'
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        send_email(email_address=settings.ADMIN_EMAIL_ADDRESS,
                   body=str(form), subject='PyWars - New user')
        new_user = authenticate(username=self.request.POST['email'],
                                password=self.request.POST['password'])
        login(self.request, new_user)
        return HttpResponseRedirect('/main/dashboard')


class ForgotPassword(TemplateView):
    template_name = 'users/forgot_password.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = AppUser.objects.filter(email=email).first()
        if user:
            user.send_password_reset_email()
        return JsonResponse({'ok': True})


class ResetPassword(FormView):
    template_name = 'users/reset_password.html'
    form_class = SetPasswordForm
    success_url = '/user/login/'

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        user = AppUser.objects.filter(pk=kwargs.get('user_id')).first()
        if user and user.password_reset_token == token:
            return super(ResetPassword, self).get(request, *args, **kwargs)
        return render(request, self.template_name, {'link_invalid': True})

    def get_form(self):
        user = AppUser.objects.filter(pk=self.kwargs.get('user_id')).first()
        form_data = self.request.POST
        if self.request.method == 'GET':
            form_data = None
        return self.form_class(user=user, data=form_data)

    def form_valid(self, form):
        form.user.password_reset_token = None
        form.save()
        return super(ResetPassword, self).form_valid(form)


class UserProfile(LoginRequiredMixin, UpdateView):
    """
    INFO: hacked a bit, so that it works with two different forms
    """
    model = AppUser
    form_class = UserSettingsForm
    password_form_class = PasswordChangeForm
    template_name = 'users/user_profile.html'
    success_url = '/user/profile/'

    def get_object(self):
        return AppUser.objects.get(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(
                            initial={'name': context['object'].name,
                                     'email': context['object'].email})
            context['switch_tab'] = True
        if 'form2' not in context:
            context['form2'] = self.password_form_class(self.request.user)
        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def form_valid(self, form):
        form.save()
        # don't logout user after password change
        update_session_auth_hash(self.request, self.request.user)
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
            form = self.get_form(form_class)
        else:
            form_name = 'form2'
            form = self.password_form_class(user=self.request.user,
                                            data=self.request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

