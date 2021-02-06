from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model= Student
        fields=['image','gender','nationality','occupation','graduated_university','stream','dob','number']

'''class LecturerRatingForm(forms.ModelForm):
    class Meta:
        model = LecturerRating
        fields = ['lecturer', 'student', 'rating']'''
