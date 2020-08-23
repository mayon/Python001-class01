from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .form import LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return HttpResponse('Hello Django!')

def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login.html', {'form': login_form, 'err': '密码错误或账号不存在'})

    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form})