from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.status == 0:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                user_status = {'user_status': True}
                return render(request, './registration/login.html',
                              context=user_status)
        else:
            #return HttpResponse("Invalid login details supplied.")
            login_failed = {'login_errors': True}
            return render(request, './registration/login.html',
                          context=login_failed)
    else:
        return render(request, './registration/login.html')

