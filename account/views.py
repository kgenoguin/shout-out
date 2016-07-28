from blog.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user = new_user)

            return render(request, 'registration/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def edit(request):
    posts = Post.objects.filter(author = request.user).order_by('-published_date')
    profile = Profile.objects.get(user = request.user)
    use = User.objects.get(username = request.user)

    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user,data = request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile,data = request.POST,files = request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')

            posts = Post.objects.filter(author = request.user).order_by('-published_date')
            profile = Profile.objects.get(user = request.user)
            use = User.objects.get(username = request.user)

            return render(request, 'account/profile.html', {'posts' : posts, 'prof' : profile, 'use' : use})

        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'posts' : posts, 'prof' : profile, 'use' : use})


@login_required
def profile(request):
    posts = Post.objects.filter(author = request.user).order_by('-published_date')
    profile = Profile.objects.get(user = request.user)
    use = User.objects.get(username = request.user)

    return render(request, 'account/profile.html', {'posts' : posts, 'prof' : profile, 'use' : use})

@login_required
def view_other_profile(request, other):
    posts = Post.objects.filter(author__username = other)
    profile = Profile.objects.get(user__username = other)
    use = User.objects.get(username = other)

    return render(request, 'account/profile.html', {'posts' : posts, 'prof' : profile, 'use' : use})
