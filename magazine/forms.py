from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CommentUser


PRODUCT_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.Form):

    quantity = forms.TypedChoiceField(choices=PRODUCT_CHOICES, coerce=int, label='Кол-во')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class RegistrationForm(UserCreationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='Почта', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2', 'email']


class AuthorizationForm(AuthenticationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CommentUserForm(forms.ModelForm):

    class Meta:

        model = CommentUser
        fields = ['comment']

        labels = {
            'name': 'Имя пользователя',
            'comment': 'Комментарий'
        }

        errors_message = {
            'mame': {
                'required': 'Поле не должно быть пустым'
            },
            'comment': {
                'required': 'Поле коммаентариев, не должно быть пустым'
            }
        }