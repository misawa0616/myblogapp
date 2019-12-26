from django import forms
from .models import Image
 
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )