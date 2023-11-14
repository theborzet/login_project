from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.models import AbstractUser
from django.views.generic.edit import CreateView
from django.views import View
from django.http import  JsonResponse


from django.urls import reverse_lazy


from common.views import TitleMixin
from users.forms import UserLoginForm, UserRegistrationForm

class IndexView(TitleMixin, TemplateView):
    title = 'Store'
    template_name = 'users/index.html'


class UserLoginView(TitleMixin, LoginView):
    title = 'Store - Авторизация'
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Получаем сессию пользователя
        session_key = self.request.session.session_key
        if not session_key:
            # Если сессия пустая, создаем новую
            self.request.session.save()
            session_key = self.request.session.session_key

        # Устанавливаем куки с уникальным значением сессии
        response = super().form_valid(form)
        response.set_cookie('session_token', session_key, secure=True)
        print(session_key)
        return response


class UserRegistrationView(TitleMixin, SuccessMessageMixin,CreateView):
    model = AbstractUser
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')
    success_message = 'Вы успешно зарегистрировались!'
    title = 'Регистрация'


class UserLogoutView(TitleMixin, LogoutView):
    title = 'Store - Выход'
    success_url = reverse_lazy('index')


class JsonUserView(TitleMixin, View):
    def get(self, request):
        user = request.user
        if ("session_token" in request.COOKIES and user.is_authenticated):
            user_data = {
                "username": user.username,
                "password": user.password,
            }
            return JsonResponse(user_data)
        else:
            error_message = {"message": "Unauthorized"}
            return JsonResponse(error_message, status=401)
