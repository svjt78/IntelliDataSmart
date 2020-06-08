from django import forms

from .models import Group


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name','description', 'purpose',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            'purpose': forms.TextInput(attrs={'class': 'textinputclass'}),
        }
