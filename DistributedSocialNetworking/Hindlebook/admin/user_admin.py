from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.forms import UserCreationForm as AdminUserCreationForm
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth import get_user_model

from Hindlebook.models import Author, Node, Settings

class UserCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = get_user_model()

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            self.Meta.model.objects.get(username__iexact=username)
        except self.Meta.model.DoesNotExist:
            return username

        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

def approve_users(modeladmin, request, queryset):
    local_node = Settings.objects.all().first().node
    for obj in queryset:
        if not Author.objects.filter(user=obj).exists():
            author = Author(user=obj, username=obj.username, node=local_node)
            author.save()
        
approve_users.short_description = "Approve user"


class UserAdmin(BaseAdmin):
    
    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    actions = [approve_users]
    
    ordering = ('username',)
    list_display = ('username', 'date_joined', 'is_approved')
    add_form = UserCreationForm


    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    
    def is_approved(self, obj):
        if Author.objects.filter(user=obj).exists():
            return True
        return False
    is_approved.short_description = 'Approved'
    is_approved.boolean = True


    
class AuthorAdmin(ModelAdmin):
    
    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []
    
    ordering = ('username',)
    list_display = ('username', 'uuid', 'date_added')

    fieldsets = (
        (None, {'fields': ('username', 'node')}),
        ('Personal', {'fields': ('about' ,'avatar', 'github_id')}),
    )

