from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_picture', 'bio')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile_picture', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
