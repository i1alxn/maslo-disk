from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from .forms import LoginForm, RegisterForm, UpdateUserForm, CreateFolderForm, UploadFileForm
from .models import File, Folder


def getFilepath(folder):
    filepath = []
    while folder.parent:
        filepath.append(folder)
        folder = folder.parent
    filepath.append(folder)
    return filepath[::-1]


@login_required(login_url='login')
def home(request):
    return render(request, 'base/home.html')


class LoginUser(LoginView):
    template_name = 'base/login_register.html'
    form_class = LoginForm
    extra_context = {'page': 'login'}

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    template_name = 'base/login_register.html'
    form_class = RegisterForm
    extra_context = {'page': 'register'}

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        root_folder = Folder.objects.create(name="root", host=user, filepaths='/root/')
        user.root_folder = root_folder
        user.save()
        return super().form_valid(form)


class UpdateUser(UpdateView):
    template_name = 'base/update_user.html'
    form_class = UpdateUserForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('home')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def folderPage(request, pk):
    user = request.user
    folder = Folder.objects.get(pk=pk)
    folder_form = CreateFolderForm()
    file_form = UploadFileForm()
    if folder.host != request.user:
        return HttpResponse('You are not allowed to view this folder')
    if request.method == 'POST':
        if 'name' in request.POST:
            folder_form = CreateFolderForm(request.POST)
            if folder_form.is_valid():
                new_folder = folder_form.save(commit=False)
                new_folder.host = request.user
                new_folder.parent = folder
                new_folder.filepaths = folder.filepaths + new_folder.name + '/'
                new_folder.save()
                return redirect('folder', pk=pk)
        file_form = UploadFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            new_file = file_form.save(commit=False)
            new_file.host = request.user
            new_file.folder = folder
            new_file.save()
            return redirect('folder', pk=pk)
    files = File.objects.filter(folder=folder)
    folders = Folder.objects.filter(parent=folder)
    filepath = getFilepath(folder)
    context = {'folder': folder, 'files': files, 'folders': folders, 'folder_form': folder_form, 'file_form': file_form,
               'filepath': filepath}
    return render(request, 'base/folder.html', context)
