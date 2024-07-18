from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager, PostManager, CommentManager
from .utils import user_directory_path
from django.conf import settings

class User(AbstractBaseUser):
    email = models.EmailField(max_length=250, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=200, unique=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True    

    def has_module_perms(self, app_label):
        return True    

    @property
    def is_staff(self):
        return self.is_admin
    


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    published = models.BooleanField(default=False)

    objects = PostManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%Y-%m-%d')}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='pcomments')
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    objects = CommentManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%Y-%m-%d')} to {self.post.slug}-{self.post.user.username}"
    

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.user.username}-{self.post.slug}"