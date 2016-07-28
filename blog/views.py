from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from account.models import Profile
from django.utils import timezone
from .forms import PostForm, CommentForm, LikeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    creators = Profile.objects.all()
    return render(request, 'blog/post_list.html', {"posts" : posts, "creators" : creators})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    return render(request, 'blog/post_detail.html', {"post" : post})


@login_required
def post_new(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.photo = form.cleaned_data["photo"]
            post.save()
            messages.success(request, 'Post successfully created!')

            return redirect('blog:post_detail', pk=post.pk)

        else:
            messages.error(request, 'Error in creating post!')
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form, 'posts' : posts})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.save()
            messages.success(request, 'Post successfully edited!')

            return redirect('blog:post_detail', pk=post.pk)
        else:
            messages.error(request, 'Editing post failed!')

    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'posts' : posts, 'post' : post})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.error(request, 'Post successfully deleted!')

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts' : posts})


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk = pk)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment successfully posted!')

            return redirect('blog:post_detail', pk=post.pk)
        else:
            messages.error(request, 'Error posting comment!')
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form, 'posts' : posts, 'post' : post})


@login_required
def like(request, pk):
    post = get_object_or_404(Post, pk = pk)

    form = LikeForm(request.POST)
    like = form.save(commit = False)
    like.post = post
    like.save()

    return redirect('blog:post_detail', pk=post.pk)
