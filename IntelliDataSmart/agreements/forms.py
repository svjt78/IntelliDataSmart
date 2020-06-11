from django import forms
from django.core.exceptions import ValidationError
from members.models import *

from .models import Agreement


class AgreementForm(forms.ModelForm):
    coverage_limit: forms.DecimalField()

    class Meta:
        model = Agreement
        exclude = ('slug',)

        fields = ('name','description', 'coverage_limit', 'group', 'product')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),

        }
