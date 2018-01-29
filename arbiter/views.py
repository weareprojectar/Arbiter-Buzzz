from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DetailView,
    DeleteView,
    ListView,
    UpdateView
)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})

@csrf_exempt
def login_view(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    if (email != '') and ('@' in email):
        username = email.split('@')[0]
        user = auth.authenticate(username=username, password=password)
    else:
        user = auth.authenticate(username=email, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponse(200)
    else:
        return HttpResponse(400)

@csrf_exempt
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
