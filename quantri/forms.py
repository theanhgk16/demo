from django import forms
from .models import Feedback
from .models import UserAvatar, Article


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class loginForm(forms.Form):
    userName = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25, widget=forms.PasswordInput)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['Content']

    Content = forms.CharField(widget=forms.TextInput(attrs={'rows': 1}))

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = UserAvatar
        fields = ['avatar']

