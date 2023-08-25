from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    available_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    @property
    def get_subfolders(self):
        return Folder.objects.filter(parent_folder=self)
    @property
    def get_subfiles(self):
        return File.objects.filter(parent_folder=self)
    @property
    def set_unavailable(self):
        self.is_available = False
        self.save()
        children = self.get_subfolders 
        for child in children:
            print("Child " + child.name)
            child.set_unavailable
        children = self.get_subfiles
        for child in children:
            print("Child " + child.name)
            child.set_unavailable
        return True


class File(models.Model):

    date_of_creation = models.DateTimeField(auto_now_add=True)
    available_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(blank=True, null=True)
    @property
    def set_unavailable(self):
        print("File set unavailable " + self.name)
        self.is_available = False
        self.save()
        print("File set unavailable " + self.name + " " + str(self.is_available))
        


class SectionType(models.Model):
    name = models.CharField(max_length=255)


class Status(models.Model):
    name = models.CharField(max_length=255)


class StatusData(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    data = models.TextField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class FileSection(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    start_line = models.IntegerField()
    end_line = models.IntegerField()
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    status_data = models.ForeignKey(StatusData, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
