from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Vote
from .forms import AddPostForm, EditPostForm, CommentForm, ReplyForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_posts.html', {'posts': posts})


def each_post(request, year, month, day, slug):
    post = get_object_or_404(Post, created__year=year, created__month=month, created__day=day, slug=slug)
    reply_form = ReplyForm()
    can_like = False
    if request.user.is_authenticated:
        if Post.can_like(self=post, user=request.user):
            can_like = True
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
    return render(request, 'posts/each_post.html',
                  {'post': post, 'comments': comments, 'form': form, 'reply_form': reply_form, 'can_like': can_like})


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


@login_required
def delete_post(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        messages.success(request, 'Your post deleted successfully', 'success')
    return redirect('accounts:user_dashboard', user_id)


@login_required
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


@login_required
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'Your reply added successfully', 'success')
            return redirect("posts:each_post", post.created.year, post.created.month, post.created.day, post.slug)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Vote(post=post, user=request.user)
    like.save()
    return redirect("posts:each_post", post.created.year, post.created.month, post.created.day, post.slug)