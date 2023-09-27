import string
import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        verification_code = self.object.email_verification_code
        self.object.is_active = False
        self.object.save()
        verification_url = self.request.build_absolute_uri(
            reverse('users:verify-email', kwargs={'verification_code': verification_code}))
        send_mail(
            'Email Verification',
            f'Перейдите по ссылке для подтверждения: {verification_url}',
            'raid_hp_auto@mail.ru',
            [self.object.email],
            fail_silently=False,
        )
        return response


class VerifyEmailView(View):
    def get(self, request, verification_code):
        user = get_object_or_404(User, email_verification_code=verification_code)
        if not user.email_verified:
            user.email_verified = True
            user.is_active = True
            user.save()
        return redirect('users:login')


class UpdatePassword(View):
    model = User
    template_name = 'users/update_password.html'
    success_url = reverse_lazy('users:login')

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('user_email')
        user = User.objects.get(email=email)

        letters_and_digits = string.ascii_letters + string.digits
        length = 8
        new_password = ''.join(random.choice(letters_and_digits) for i in range(length))

        send_mail(
            'Email changed password',
            f'ваш новый пароль: {new_password}',
            'raid_hp_auto@mail.ru',
            [user.email],
            fail_silently=False,
        )
        user.set_password(new_password)
        user.save()

        return redirect('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
