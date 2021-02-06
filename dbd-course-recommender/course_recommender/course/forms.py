from django import forms
from .models import *


class CourseEnrollForm(forms.ModelForm):
    student = forms.IntegerField(required=False)
    status = forms.IntegerField(required=False)

    class Meta:
        model = Enrollment
        fields = ['student', 'status']


class CourseDismissForm(forms.ModelForm):
    student = forms.IntegerField(required=False)

    class Meta:
        model = Enrollment
        fields = ['course', 'student']

class CommentForm(forms.ModelForm):
    class Meta:
        model = SubjectRating
        fields = [ 'rating', 'comment']