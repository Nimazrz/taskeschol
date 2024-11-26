from django import forms
from django.contrib.auth.models import User

from account.models import *


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ('username', 'first_name', 'last_name', 'meli_code', 'school', 'bio', 'is_teacher')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return password

    def clean_meli_code(self):
        meli_code = self.cleaned_data.get('meli_code')
        if meli_code != "":
            if meli_code.isdigit():
                if Teacher.objects.filter(meli_code=meli_code).exists():
                    raise forms.ValidationError('این کد میلی قبلا استفاده شده')
                return meli_code
            else:
                raise forms.ValidationError("لطفا یک کد ملی معتبر وارد کنید")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True, widget=forms.TextInput)
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)
