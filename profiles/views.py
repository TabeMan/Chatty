from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import Profile
from django.shortcuts import redirect
from django.contrib.auth import login
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, ProfileForm


class CustomLoginView(LoginView):
    template_name = 'profiles/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('chat:home')


class RegisterView(FormView):
    template_name = 'profiles/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('chat:home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('chat:home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        if user is not None:
            Profile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                slug=slugify(user.username),
            )

            login(self.request, user,
                  backend='django.contrib.auth.backends.ModelBackend')

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/account.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return Profile.objects.get(slug=self.kwargs.get('profile_slug'))


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profiles/edit_account.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return Profile.objects.get(slug=self.kwargs.get('profile_slug'))

    def get_success_url(self):
        return reverse_lazy('profiles:profile', kwargs={'slug': self.object.slug})
