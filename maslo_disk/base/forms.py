from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django import forms
from .models import Folder, File


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']


class UpdateUserForm(ModelForm):
    delete_avatar = forms.BooleanField(required=False, label='delete photo')

    class Meta:
        model = get_user_model()
        fields = ['username', 'avatar']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('delete_avatar'):
            user.avatar.delete()
            user.avatar = 'avatars/avatar.svg'
        if commit:
            user.save()
            self.save_m2m()
        return user


class CreateFolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name']


class UploadFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']
