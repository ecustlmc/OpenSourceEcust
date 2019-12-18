from django.shortcuts import render,redirect
from django.conf import settings
from app_report import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
SITE_TITLE = settings.SITE_TITLE
BAR_TITLE = settings.SITE_TITLE
def render_with_global(req,templates,dic):
    dic["SITE_TITLE"] = SITE_TITLE
    dic["BAR_TITLE"] = BAR_TITLE
    return render(req,templates,dic)

# Create your views here.
def register(req):
    if req.method == "POST":
        form = forms.RegisterForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            User.objects.create_user(username=username,password=password)
            return redirect(req,"/report/login/")
        else:
            return render_with_global(req,"app_report/register.html",locals())
    else:
        form = forms.RegisterForm()
        return render_with_global(req,"app_report/register.html",locals())

def _login(req):
    if req.method == "POST":
        form = forms.LoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data["password"]
            user = authenticate(req,username=username,password=password)
            if user is None:
                form.password.error_messages = "密码错误"
                return render_with_global(req,"app_report/login.html",locals())
            else:
                login(req,user)
                return redirect('/report/index/')
        else:
            return render_with_global(req,"app_report/login.html",locals())
    else:
        form = forms.LoginForm()
        return render_with_global(req,"app_report/login.html",locals())

@login_required
def index(req):
    return render_with_global(req,"app_report/index.html",locals())