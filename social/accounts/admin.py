from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm, PostForm
from .models import User, Post, Comment, Vote
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display= ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets=(
        (None,{'fields':('email', 'phone_number', 'username', 'password')}),
        ('Permision',{'fields':('is_active', 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        (None,{'fiels':('email', 'phone_number', 'username', 'password1', 'password2')}),
    )

    search_fields= ('email', 'phone_number')
    ordering = ('email', )
    filter_horizontal =()
    list_per_page=3


class PostAdmin(admin.ModelAdmin):
    form = PostForm

    list_display= ('created','user',  'title', 'published')
    list_filter = ('published',)

    fieldsets=(
        (None,{'fields':('title', 'description', 'image', 'published')}),
        
    )
    search_fields= ('title', 'user')
    ordering = ('created', )

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'like', 'dislike')

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Vote, VoteAdmin)
