from django import forms
from django.contrib.auth.models import User
from app_report import models
class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=50)
    name = forms.CharField(label="姓名",max_length=50)
    password1 = forms.CharField(label="密码",widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码",widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 4:
            raise forms.ValidationError("用户名必须大于4个字符")
        elif len(username) > 50:
            raise forms.ValidationError("用户名必须小于50个字符")
        else:
            Q_res = User.objects.filter(username__exact=username)
            if len(Q_res) > 0:
                raise forms.ValidationError("用户名已经存在，再试试？")
            else:
                return username

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 1:
            raise forms.ValidationError("姓名不能为空")
        elif len(name) > 50:
            raise forms.ValidationError("姓名过长")
        else:
            return name

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("密码过短")
        elif len(password1) > 20:
            raise forms.ValidationError("密码过长")
        else:
            return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("前后两次密码输入的不一致")
        return password2

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'form-control'



class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=50)
    password = forms.CharField(label="密码",max_length=18,widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        user_list = User.objects.filter(username__exact=username)
        if len(user_list) == 0:
            raise forms.ValidationError("用户名不存在")
        else:
            return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        return password

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'form-control'

class passwordchangeForm(forms.Form):
    oldpassword = forms.CharField(label="旧密码",max_length=18,widget=forms.PasswordInput)
    password1 = forms.CharField(label="新密码",max_length=18,widget=forms.PasswordInput)
    password2 = forms.CharField(label="新密码确认",max_length=18,widget=forms.PasswordInput)
    def clean_oldpassword(self):
        oldpassword = self.cleaned_data["oldpassword"]
        return oldpassword

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("密码过短")
        elif len(password1) > 20:
            raise forms.ValidationError("密码过长")
        else:
            return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("前后两次密码输入的不一致")
        return password2

    def __init__(self, *args, **kwargs):
        super(passwordchangeForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'form-control'

class newReportForm(forms.Form):
    title = forms.CharField(max_length=50)
    tag = forms.ChoiceField(choices=models.report_tag)
    content = forms.CharField(widget=forms.Textarea(attrs = {"row":10}))

    def __init__(self, *args, **kwargs):
        super(newReportForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'form-control'
