from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import random

class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, username, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, username, password=None):
        user = self.create_user(
            email,
            phone_number=phone_number,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class PostManager(models.Manager):
    def create_post(self, user, title, image, description, slug, published=False):
        if not title:
            raise ValueError('The post must have a title')
        if not image:
            raise ValueError('The post must have an image')
        if not description:
            raise ValueError('The post must have a description')

        created_time = timezone.now()

        post = self.model(
            user=user,
            title=title,
            image=image,
            description=description,
            created=created_time,
            slug=slug,
            published=published,
            
        )
        post.save(using=self._db)
        return post
    

class CommentManager(models.Manager):
    def create_comment(self, user, post, body, published=False):
        if not body:
            raise ValueError('The comment most have text')
        
        comment = self.model(
            user = user,
            post = post,
            body = body,
            created = timezone.now(),
            published = published
        )
        comment.save(using=self._db)
        return comment
    
