from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from posts.models import Post
from django.contrib.auth.decorators import login_required


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