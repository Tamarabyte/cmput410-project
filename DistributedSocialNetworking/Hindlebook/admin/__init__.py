from django.contrib import admin
from Hindlebook.models import Post, Comment
from Hindlebook.admin.user_admin import UserAdmin
from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

# Register your models here.
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)