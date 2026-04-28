import pytz
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, UpdateView

from config import settings
from users.forms import RegisterForm, EmailVerificationForm, LoginForm, AccountsModelForm
from users.models import VerificationCodeModel, AccountsModel

UserModel = get_user_model()


class AccountView(LoginRequiredMixin,UpdateView):
    template_name = 'users/acount.html'
    form_class = AccountsModelForm
    success_url = reverse_lazy('users:account')
    context_object_name = 'account'
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        account, _ = AccountsModel.objects.get_or_create(user=self.request.user)
        return account


def send_email_verification(user):
    random_code = random.randint(100000, 999999)

    if VerificationCodeModel.objects.filter(code=random_code).exists():
        send_email_verification(user)
    else:
        VerificationCodeModel.objects.create(code=random_code, user=user)
        try:
            send_mail(
                'Verification code',
                f'Your verification code is {random_code}.',
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            return True
        except Exception as e:
            print(e)
            return False


class CartView(TemplateView):
    template_name = 'users/cart.html'


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('pages:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        print("Form is valid")  # Debug statement
        print(f"Username: {username}, Password: {password}")  # Debug statement

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            print(f"User authenticated: {user}")  # Debug statement
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid username or password.')
            print("Authentication failed")  # Debug statement
            return self.form_invalid(form)

    def form_invalid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        messages.error(self.request, 'Form is invalid')
        print("Form is invalid")  # Debug statement
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:verify-email')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_email_verification(user)
        return super().form_valid(form)

    def form_invalid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


def verify_email(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user_code = VerificationCodeModel.objects.filter(code=code).first()
            if user_code:
                now = datetime.now(pytz.timezone(settings.TIME_ZONE))
                send_time = user_code.created_at.astimezone(pytz.timezone(settings.TIME_ZONE)) + timedelta(minutes=2)
                if now < send_time:
                    user = UserModel.objects.filter(pk=user_code.pk).first()
                    if user:
                        user.is_active = True
                        user.save()
                    return redirect(reverse_lazy('users:login'))
                else:
                    messages.error(request, 'Your verification code has expired.')
            else:
                messages.error(request, 'Your verification code is invalid.')

        else:
            messages.error(request, form.errors)
    return render(request, 'users/verify-email.html')


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('pages:home')


class Reset_PasswordView(TemplateView):
    template_name = 'users/reset-password.html'


class WishListView(TemplateView):
    template_name = 'users/wishlist.html'


class CheckoutView(TemplateView):
    template_name = 'products/checkout.html'
