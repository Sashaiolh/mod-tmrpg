# import form class from django 
from django import forms 


# import GeeksModel from models.py 
from .models import *
   
# create a ModelForm 
class ModerRegForm(forms.ModelForm):
    secret_code = forms.CharField(label='Код', max_length=20)
    attrs = {
        "type": "password",
        'class': 'form-control'
    }
    # password = forms.CharField(label='Пароль',widget=forms.TextInput(attrs=attrs))
    # password2 = forms.CharField(label='Повторите пароль',widget=forms.TextInput(attrs=attrs))
    # class Meta:
    #     model = RegisterFormModel
    #     fields = ('secret_code', 'password1', 'password2',)
    class Meta:
        model = RegisterFormModel
        widgets = {
        'password1': forms.PasswordInput(),
        'password2': forms.PasswordInput(),
        
        }
        fields = ('secret_code','password1','password2',)