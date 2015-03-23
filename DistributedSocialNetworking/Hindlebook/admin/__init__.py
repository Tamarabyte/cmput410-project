from django.contrib import admin
from django.contrib.auth.models import Group

from Hindlebook.models import Author, Post, Comment, Settings, Node, Category
from Hindlebook.admin.user_admin import UserAdmin, AuthorAdmin
from Hindlebook.admin.post_admin import PostAdmin, CategoryAdmin
from Hindlebook.admin.server_admin import SettingsAdmin, NodeAdmin

from django.contrib.auth import get_user_model
User = get_user_model()

# Register your models here
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Category, CategoryAdmin)
