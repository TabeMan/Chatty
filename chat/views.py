from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import ChatRoom, ChatMessage
from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateRoomForm


class HomeView(TemplateView):
    template_name = 'chat/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = ChatRoom.objects.all()
        search_query = self.request.GET.get('q', None)
        if search_query:
            context['rooms'] = context['rooms'].filter(
                name__icontains=search_query)
        return context


class RoomView(DetailView):
    model = ChatRoom
    template_name = 'chat/room.html'
    context_object_name = 'room'

    def get_object(self, queryset=None):
        return ChatRoom.objects.get(slug=self.kwargs.get('room_slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = ChatMessage.objects.filter(
            room=self.get_object())
        context['users'] = self.get_object().users.all()
        return context


class CreateRoomView(LoginRequiredMixin, CreateView):
    model = ChatRoom
    form_class = CreateRoomForm
    template_name = 'chat/create_room.html'
    success_url = reverse_lazy('chat:home')
    
    def form_valid(self, form):
        room = form.save(commit=False)
        room.slug = slugify(room.name)
        print(room.slug)
        room.save()
        return super().form_valid(form)
