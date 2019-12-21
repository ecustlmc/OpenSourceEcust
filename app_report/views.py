from django.shortcuts import render,redirect
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from app_report import forms
from app_report.models import Report,ReportFile,ReportLikes,ReportComments
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.views.generic import ListView
from django.core.paginator import Paginator
import datetime
from django.forms import ValidationError

SITE_TITLE = settings.SITE_TITLE
BAR_TITLE = settings.SITE_TITLE
def add_global(loc):
    loc["SITE_TITLE"] = SITE_TITLE
    loc["BAR_TITLE"] = BAR_TITLE
    return loc

# Create your views here.
def register(req):
    if req.method == "POST":
        form = forms.RegisterForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            name = form.cleaned_data['name']
            user = User.objects.create_user(username=username,password=password)
            user.first_name = name#不用Last_name
            user.save()
            return render(req,"app_report/registersuccess.html",add_global(locals()))
        else:
            return render(req,"app_report/register.html",add_global(locals()))
    else:
        form = forms.RegisterForm()
        return render(req,"app_report/register.html",add_global(locals()))

def _login(req):
    if req.method == "POST":
        form = forms.LoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data["password"]
            user = authenticate(req,username=username,password=password)
            if user is None:
                form.add_error('password',ValidationError("密码错误"))
                return render(req,"app_report/login.html",add_global(locals()))
            else:
                login(req,user)
                return redirect('/report/index/')
        else:
            return render(req,"app_report/login.html",add_global(locals()))
    else:
        form = forms.LoginForm()
        return render(req,"app_report/login.html",add_global(locals()))

@login_required
def _logout(req):
    logout(req)
    return redirect("/report/login/")

class ReportListView(ListView):
    queryset = Report.objects.filter().order_by('-time')
    paginate_by = settings.NUMBER_OF_PER_PAGE

@login_required
def index(req):
    reports = Report.objects.filter().order_by('-time')
    paginator = Paginator(reports,settings.NUMBER_OF_PER_PAGE)
    page = req.GET.get("page")
    page_obj = paginator.get_page(page)
    is_paginated = True
    return render(req,"app_report/index.html",add_global(locals()))

@login_required
def ajax_like(req):
    if req.is_ajax():
        report_id = dict(req.POST).get("report_id")[0]
        report = Report(id=int(report_id))
        obj,created = ReportLikes.objects.get_or_create(user = req.user,report = report)
        if created:
            obj.like = 1
            obj.save()
            return JsonResponse({"status":"1"})
        else:
            return JsonResponse({"status":"0"})


@login_required
def ajax_comment(req):
    if req.is_ajax():
        report_id = dict(req.POST).get("report_id")[0]
        comment = dict(req.POST).get("comment")[0]
        report = Report(id = int(report_id))
        obj = ReportComments(user=req.user,comment=comment,report=report,time=datetime.datetime.now())
        obj.save()
        return JsonResponse({"status":"1"})

@login_required
def changepassword(req):
    if req.method == "POST":
        form = forms.passwordchangeForm(req.POST)
        if form.is_valid():
            oldpassword = form.cleaned_data["oldpassword"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            user = authenticate(req,username = req.user.username,password = oldpassword)
            if user is None:
                form.add_error('oldpassword',ValidationError("密码错误"))
                return render(req,"app_report/changepaasword.html",add_global(locals()))
            else:
                user = req.user
                user.set_password(password2)
                user.save()
                logout(req)
                return redirect("/report/login/")
        else:
            return render(req,"app_report/changepaasword.html",add_global(locals()))
    else:
        form = forms.passwordchangeForm()
        return render(req,"app_report/changepaasword.html",add_global(locals()))

@login_required
def reportview(req):
    if req.method == "POST":
        pass
    else:
        reports = Report.objects.filter(user=req.user).order_by('-time')
        paginator = Paginator(reports,settings.NUMBER_OF_PER_PAGE)
        page = req.GET.get("page")
        page_obj = paginator.get_page(page)
        is_paginated = True
        return render(req,"app_report/reportview.html",add_global(locals()))

@login_required
def reportnew(req):
    if req.method == "POST":
        form = forms.newReportForm(req.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            tag = form.cleaned_data["tag"]
            content = form.cleaned_data["content"]
            now = datetime.datetime.now()
            newReport = Report(user=req.user,title=title,tag=tag,content=content,time=now)
            newReport.save()
            for each in req.FILES.getlist("file"):
                newReportFile = ReportFile(report = newReport,file=each)
                newReportFile.save()
            return HttpResponse(dict(req.POST))
        else:
            return HttpResponse("ERROR FORM")
    else:
        form = forms.newReportForm()
        return render(req,"app_report/reportnew.html",add_global(locals()))
