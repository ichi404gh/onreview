from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from onreview_app.forms import *
from django.contrib.auth.models import User
from django.urls import reverse
def login_request(request):
    if(request.method == 'GET'):
        context={
            'next':request.GET.get('next','/'),
            'form':AuthenticationForm(request)
        }

        return render(request, 'login.html', context)
    else:
        form = AuthenticationForm(None, request.POST or None)
        if(form.is_valid()):
            login(request, form.get_user())
            return redirect(request.POST['next'] or '/', permanent=False)
        return redirect(reverse("login"), permanent=False)

def logout_request(request):
    logout(request)
    return redirect(request.GET.get('next','/'), permanent=False)

def register(request):
    form = RegisterForm(request.POST or None)
    if(request.method == 'GET'):
        return render(request, 'register.html', {'form': form})
    else:
        if(form.is_valid()):
            try:
                u=User.objects.create_user(
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password']
                                )
                u = authenticate(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password']
                        )
                if(u is not None and u.is_active):
                    login(request, u)
            except Exception as e:
                return render(request, 'register.html', {'form': form, 'error':e})

        return redirect('/', permanent=False)
