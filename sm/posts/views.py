from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import AddPostForm, EditPostForm, CommentForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_posts.html', {'posts': posts})


def each_post(request, year, month, day, slug):
    post = get_object_or_404(Post, created__year=year, created__month=month, created__day=day, slug=slug)
    comments = Comment.objects.filter(post=post, is_reply=False)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your comment added successfully', 'success')
    else:
        form = CommentForm()
    return render(request, 'posts/each_post.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def add_post(request, user_id):
    if request.user.id == user_id:
        if request.method == "POST":
            form = AddPostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.slug = slugify(form.cleaned_data['body'][:30])
                new_post.save()
                messages.success(request, 'Your post added successfully', 'success')
                return redirect('accounts:user_dashboard', user_id)
        else:
            form = AddPostForm()
        return render(request, 'posts/add_post.html', {'form': form})
    else:
        return redirect("posts:all_posts")


def delete_post(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        messages.success(request, 'Your post deleted successfully', 'success')
    return redirect('accounts:user_dashboard', user_id)


def edit_post(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, pk=post_id)
        if request.method == "POST":
            form = EditPostForm(request.POST, instance=post)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.slug = slugify(form.cleaned_data['body'][:30])
                new_post.save()
                messages.success(request, 'Your post edited successfully', 'success')
                return redirect('accounts:user_dashboard', user_id)
        else:
            form = EditPostForm(instance=post)
        return render(request, 'posts/edit_post.html', {'form': form})
    else:
        return redirect('posts:all_post')
