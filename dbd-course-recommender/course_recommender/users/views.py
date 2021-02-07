import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from course.models import *
from course.services import get_enrolled_subjects, get_recommmendations
from .forms import  *
from .models import Student


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            messages.success(
                request, f'Please Update your profile first.')
            return redirect('users-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    account = get_object_or_404(Student, account = request.user)
    context = {'home_page': 'active',
                'account' : account,
                 }
    return render(request, 'users/profile.html', context)

@login_required
def EditProfile(request):
    student = get_object_or_404(Student, account = request.user)
    if request.method == "POST":
        p_form = EditProfileForm(request.POST,request.FILES, instance= student)
        u_form = UserUpdateForm(request.POST, instance= request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('users-profile')
        else:
            messages.error(request, p_form.errors)
            messages.error(request, u_form.errors)
    else:
        p_form= EditProfileForm()
        u_form =UserUpdateForm()
        context={'p_form': p_form, 'u_form': u_form}
        return render(request, 'users/update-profile.html', context )



