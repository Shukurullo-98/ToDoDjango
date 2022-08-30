from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task
from django.views import View
from .form import PositionForm
from django.db import transaction


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed=False).count()
        search_task = self.request.GET.get('search') or ''
        if search_task:
            context['tasks'] = context['tasks'].filter(title__contains=search_task)
        context['search_task'] = search_task
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'mainapp/task_detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasks')


class Login(LoginView):
    template_name = 'mainapp/login.html'
    fields = ['title', 'description', 'completed']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class Register(FormView):
    template_name = 'mainapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    # regdan otgan bolsa login oynaga otkazmaydi
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register, self).get(*args, **kwargs)


# class TaskReorder(View):
#     def post(self, request):
#         form = PositionForm(request.POST)
#         if form.is_valid():
#             positionList = form.cleaned_data['position'].split(',')
#
#             with transaction.atomic():
#                 self.request.user.set_task_order(positionList)
#         return redirect(reverse_lazy('tasks'))
