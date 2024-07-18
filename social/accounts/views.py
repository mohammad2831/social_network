from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm,  UserLoginForm, PostForm, CommentForm
from . models import User, Post, Comment, Vote
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

class UserRegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    form_class = UserRegistrationForm
    def get(self, request):
        
        form = self.form_class
        return render(request, 'accounts/register.html', {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['email'], cd['phone'], cd['full_name'], cd['password'])
            messages.success(request, 'you registered succesfuli', 'success')
            return redirect('home:home')
        return render(request,'accounts/register.html', {'form':form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logout succes ', 'success')
        return redirect('home:home')

class UserLoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    form_class = UserLoginForm

    def get(self, request):
        
        form = self.form_class()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                return redirect('home:home')
            
            messages.error(request, 'Email or password is wrong', 'danger')

        return render(request, 'accounts/login.html', {'form': form})
    

class CreatePostView(LoginRequiredMixin, View):
    form_class = PostForm

    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        form = self.form_class()
        return render(request, 'accounts/profile.html', {'user':user ,'form': form})

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create_post(
                user=request.user,
                title=form.cleaned_data['title'],
                image=form.cleaned_data['image'],
                description=form.cleaned_data['description'],
                slug=form.cleaned_data['slug']
            )
            return redirect('accounts:user_profile', username=user.username)
        return render(request, 'accounts/profile.html', {'form': form, 'user':user})
    


class CreateCommentView(LoginRequiredMixin, View):

    form_class = CommentForm

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug, published=True)
        comments = post.pcomments.filter(published=True)
        form = self.form_class()
        return render(request, 'accounts/comment.html', {'post': post, 'comments': comments, 'form': form})
    
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, published=True)
        form = self.form_class(request.POST)
        if form.is_valid():
            Comment.objects.create_comment(
            user = request.user,
            post = post,
            body = form.cleaned_data['body'],
            )
            messages.success(request, 'Your comment has been added.')
            return redirect('accounts:create_comment', slug=post.slug)
        comments = post.pcomments.filter(published=True)
        return render(request, 'accounts/comment.html', {'post': post, 'comments': comments, 'form': form})



class PostLikeView(LoginRequiredMixin, View):

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'You have already liked this post', 'danger')
        else:
            Vote.objects.create(post=post, user=request.user, like=True, dislike=False)
            messages.success(request, 'You liked this post', 'success')
        return redirect('home:home')

class PostDislikeView(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'You send your vote', 'danger')
        else:
            Vote.objects.create(post=post, user=request.user, like= False, dislike=True)
            messages.success(request, 'You disliked this post', 'success')
        return redirect('home:home')