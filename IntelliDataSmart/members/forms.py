from django import forms

from .models import Member


class MemberForm(forms.ModelForm):
    age: forms.IntegerField()
    class Meta:
        model = Member
        exclude = ('slug',)
        #fields = ('name', 'age')
        #fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),

        }
