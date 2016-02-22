from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from onreview_app.forms import *
from django.contrib.auth.models import User

def login_request(request):
    if(request.method == 'GET'):
        context={
        'next':request.GET.get('next','/'),
        'form':AuthenticationForm(request)
        }
        return render(request, 'login.html', context)
    else:
        form = AuthenticationForm(None, request.POST or None)
        print(dir(form))
        redirect_to = request.POST['next']
        if(form.is_valid()):
            login(request, form.get_user())
            return redirect(redirect_to, permanent=False)

        return redirect(LOGIN_URL, permanent=False)

def logout_request(request):
    logout(request)
    return redirect(request.GET.get('next','/'), permanent=False)

def register(request):
    if(request.method == 'GET'):
        form = RegisterForm(request.POST or None)
        return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm(request.POST or None)
        if(form.is_valid()):
            try:
                u=User.objects.create_user(
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password']
                                )
                u = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'])
                if(u is not None):
                    if(u.is_active):
                        login(request, u)
                    else:
                        print('not active')
                else:
                    print('none')
            except Exception as e:
                print(type(e))
                print(e)
                return render(request, 'register.html', {'form': form, 'error':e})

        return redirect('/', permanent=False)
