from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {"posts" : posts})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    return render(request, 'blog/post_detail.html', {"post" : post})


@login_required
def post_new(request):
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
    return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.photo = form.cleaned_data["photo"]
            post.save()
            messages.success(request, 'Post successfully edited!')

            return redirect('blog:post_detail', pk=post.pk)
        else:
            messages.error(request, 'Editing post failed!')

    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.error(request, 'Post successfully deleted!')

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts' : posts})
