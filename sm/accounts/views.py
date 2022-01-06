from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserLoginForm, EditProfile, PhoneLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from posts.models import Post
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                return redirect('posts:all_posts')
            else:
                messages.error(request, 'Username or Password is wrong try again', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/user_login.html', {'form': form})


def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            login(request, user)
            messages.success(request, 'You registered successfully', 'success')
            return redirect('posts:all_posts')
        else:
            messages.error(request, 'Registration failed try again', 'danger')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/user_register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('posts:all_posts')


@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(user=user_id)
    self_dash = False
    if request.user.id == user_id:
        self_dash = True
    return render(request, 'accounts/user_dashboard.html', {'user': user, 'posts': posts, 'self_dash': self_dash})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=user.profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.phone = form.cleaned_data['phone']
            new_form.save()
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Your profile edited successfully', 'success')
            return redirect('accounts:user_dashboard', user_id)
    else:
        form = EditProfile(instance=user.profile, initial={'email': request.user.email})
    return render(request, 'accounts/edit_profile.html', {'form': form})


def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone = f"0{form.cleaned_data['phone']}"
            rand_number = randint(1000, 9999)
            api = KavenegarAPI('374A676B4F374D397346574466655235723773336E4977'
                               '76574255647743694C476370676E36432F414F4D3D')
            params = {'receptor': phone, 'message': rand_number}
            api.sms_send(params)
            messages.success(request, 'sms sent to your phone', 'success')

    else:
        form = PhoneLoginForm()
    return render(request, 'accounts/phone_login.html', {'form': form})
