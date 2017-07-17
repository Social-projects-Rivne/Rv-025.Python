from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def login_view(request):
"""Checks whether user exists in database and has permissions to login.
"""
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        message = None
        if user is not None:
            if user.status == 0:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                message = ("Your account doesn't have access to this page."
                           "To proceed, please login with an account "
                           "that has access.")
        else:
            message = ("Your username and password didn't match. "
                       "Please try again.")
            context = { "message": message }
        return render(request, './registration/login.html', context=context)
    else:
        return render(request, './registration/login.html')

