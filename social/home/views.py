from django.shortcuts import render
from django.views import View
from accounts.models import Post



class HomeView(View):
    def get(self, request):
        posts = Post.objects.filter(published=True)
        return render(request, 'home/home.html', {'posts': posts})