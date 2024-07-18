# utils.py
import os
from django.utils.text import slugify
from datetime import datetime

def user_directory_path(instance, filename):
   
    username_slug = slugify(instance.user.username)
    now = datetime.now()
    path = os.path.join(
        'post', 
        username_slug, 
        now.strftime('%Y'), 
        now.strftime('%m'), 
        now.strftime('%d')
    )
    return os.path.join(path, filename)
