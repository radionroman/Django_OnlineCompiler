from django import forms
from .models import Folder, File


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class AddFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']
        widgets = {'parent_folder': forms.Select(attrs={'class': 'form-control'})}


class AddFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'description', 'owner', 'is_available', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }