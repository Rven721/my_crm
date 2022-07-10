"""Here forms lives"""
from django import forms

class FileUploadForm(forms.Form):
    """Form to upload file"""
    base_data = forms.FileField(label="Исходные данные")
