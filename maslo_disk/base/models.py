from django.contrib.auth.models import AbstractUser
from django.db import models


def get_file_upload_path(instance, filename):
    return f'{instance.host.id}{instance.folder.filepaths}{filename}'


class Folder(models.Model):
    name = models.CharField(max_length=255)
    host = models.ForeignKey('User', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    filepaths = models.TextField(default='')

    def __str__(self):
        return self.name


class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    host = models.ForeignKey('User', on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_file_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name


class User(AbstractUser):
    avatar = models.ImageField(null=True, default="avatars/avatar.svg", upload_to="avatars/",
                               verbose_name="Profile photo")
    available_files = models.ManyToManyField('File', related_name='available_files')
    root_folder = models.OneToOneField('Folder', on_delete=models.CASCADE, related_name='root_folder', null=True)

    def __str__(self):
        return self.username
