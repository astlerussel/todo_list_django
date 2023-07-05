# todo_list/todo_app/views.py
from django.urls import reverse, reverse_lazy
from django.views import View
from django.forms import DateInput
from django import forms
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import ToDoItem, ToDoList

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth

class ItemDone(View):
    def post(self, request, list_id, pk):
        todo_item = ToDoItem.objects.get(id=pk)
        todo_item.is_completed = True
        todo_item.save()
        return redirect("list", list_id=list_id)
    
class ItemStart(View):
    def post(self, request, list_id, pk):
        todo_item = ToDoItem.objects.get(id=pk)
        todo_item.in_progress = True
        todo_item.save()
        return redirect("list", list_id=list_id)

def logout_user(request):
    auth.logout(request)
    return redirect('login_user') 

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email =request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email is exist ')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username,
password=password, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                print("success")
                return redirect('login_user')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        print("no post method")
        return render(request, 'todo_app/user_registration.html')
    

def login_user(request):
    if request.method == 'POST':
        username =request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')
    else:
        return render(request, 'todo_app/login.html') 


class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"



class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        queryset = ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

        sort_by = self.request.GET.get('sort_by')

        if sort_by == 'priorityh':
            queryset = queryset.order_by('priority')
        elif sort_by == 'priorityl':
            queryset = queryset.order_by('-priority')
        elif sort_by == 'due_date':
            queryset = queryset.order_by('due_date')
        else:
            queryset = queryset.order_by('priority')

        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["sort_by"] = self.request.GET.get('sort_by')
        return context


class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Add a new To-Do List"
        return context

class ToDoItemForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = [
            "todo_list",
            "title",
            "description",
            "due_date",
            "priority",
        ]
        widgets = {
            'due_date': DateInput(attrs={'type': 'date'})
        }

class ItemCreate(CreateView):
    model = ToDoItem
    form_class = ToDoItemForm

    def get_initial(self):
        initial_data = super().get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super().get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create New Task"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit Task"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ListDelete(DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("home")


class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
