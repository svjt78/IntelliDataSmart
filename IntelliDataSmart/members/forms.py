from django import forms
from django.core.exceptions import ValidationError
from members.models import *

from .models import Member


class MemberForm(forms.ModelForm):
    age: forms.IntegerField()
    # this function will be used for the validation
    def clean(self):

                # data from the form is fetched using super function
                super(MemberForm, self).clean()

                # extract the username and text field from the data
                age = self.cleaned_data.get('age')

                # age range check
                if (age <= 0 or age >= 100):
                    self._errors['age'] = self.error_class([
                        'Age is valid only in range of 1 and 99'])

                # return any errors if found
                return self.cleaned_data


    class Meta:
        model = Member
        exclude = ('slug',)
        #fields = ('name', 'age')
        #fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'creator': forms.TextInput(attrs={'readonly':'readonly'}),
        }
