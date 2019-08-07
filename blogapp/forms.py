from django.forms import ModelForm, Form
from django import forms
from .models import *

# class ProfileForm(Form):
#     name = forms.CharField(widget=forms.TextInput(), label='Имя')
#     email = forms.EmailField (widget=forms.EmailInput())
#     password = forms.CharField(widget=forms.PasswordInput())
#
#     b_day = forms.DateField(widget=forms.DateInput(format='%m/%d/%Y'), label='День рождения')
#     skype = forms.CharField(widget=forms.TextInput())
#     facebook = forms.URLField(widget=forms.URLInput())
#     about = forms.CharField(widget=forms.Textarea(), label='Пару слов о себе')




class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        # widgets = {'password': forms.PasswordInput}


# class LoginForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         widgets = {'password': forms.PasswordInput}

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [ 'b_day', 'skype', 'facebook', 'about']
        widgets = {'b_day': forms.SelectDateWidget(years=range(1930,2010))}


# class PostForm(ModelForm):
#     class Meta:
#         model = Post
#         fields = [ 'title', 'post']