from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View, TemplateView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistionForm, UserLoginForm


def HomeView(request):
    films = Film.objects.all().order_by("-id")
    context = {
        'films': films,
    }
    return render(request, 'home.html', context)


def FilmList(request):
    films = Film.objects.all().order_by("-id")
    context = {
        'films': films,
    }
    return render(request, 'film_list.html', context)

def FilmDetail(request,id):
    film_detail = Film.objects.get(id=id)

    context = {
        'film_detail': film_detail,
    }

    return render(request, 'film_detail.html', context)


class UserRegistionView(CreateView):
    form_class = UserRegistionForm
    template_name = 'register.html'
    success_url = reverse_lazy('Home')

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("Home")

class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('Home')

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Tài khoản không tồn tại"})

        return super().form_valid(form)

