from django.contrib import admin
from Hindlebook.models import Post, User, Comment
from Hindlebook.admin.user_admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)