from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from message.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['status', 'image']


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email', 'password']
        widgets = {
            "password": forms.PasswordInput
        }

    retype_password = forms.CharField(widget=forms.PasswordInput)

    def clean_retype_password(self):

        password = self.cleaned_data['password']
        retype_password = self.cleaned_data['retype_password']

        if password != retype_password:
            raise ValidationError('The passwords do not match!')

        return retype_password

    def save(self, commit=True):

        new_user = super(RegisterForm, self).save(commit=False)
        new_user.set_password(self.cleaned_data['password'])

        if commit:
            new_user.save()

        return new_user
