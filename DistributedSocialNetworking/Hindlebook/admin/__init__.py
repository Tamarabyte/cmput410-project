from django.contrib import admin
from django.contrib.auth.models import Group

from Hindlebook.models import Post, Comment, Server, Node, Category
from Hindlebook.admin.user_admin import UserAdmin
from Hindlebook.admin.post_admin import PostAdmin, CategoryAdmin
from Hindlebook.admin.server_admin import ServerAdmin, NodeAdmin

from django.contrib.auth import get_user_model
User = get_user_model()

# Register your models here
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Category, CategoryAdmin)
