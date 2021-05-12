from django.http.response import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from todo.models import Task

from django.contrib.auth.mixins import LoginRequiredMixin
# After this import you have to set the LOGIN_URL = 'login'
# inside the setting.py file


class TaskList(LoginRequiredMixin, generic.ListView):
    model = Task
    # template_name  =  'task_list.html'
    context_object_name = 'tasks'

    # This code below makes each user see what belongs to them
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context['tasks'].filter(user=self.request.user)
        context["count"] = context['tasks'].filter(complete=False).count()

        #To search things we have in our database
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        return context


class TaskView(LoginRequiredMixin, generic.DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'


class TaskCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    # This function stops a user from creating a task in the name of another user (ForeignKey)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, generic.DeleteView):
    model = Task
    context_object_name = 'task'
    # template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
