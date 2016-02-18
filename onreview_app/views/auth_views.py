from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


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
