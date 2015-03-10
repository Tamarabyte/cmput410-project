from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.forms import UserCreationForm as AdminUserCreationForm
from django.contrib.auth import get_user_model


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
        queryset.update(is_active=True)
approve_users.short_description = "Approve user registrations"

class UserAdmin(BaseAdmin):
    
    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []
    actions = [approve_users]
    
    ordering = ('username',)
    list_display = ('username', 'uuid', 'date_joined', 'is_active')
    add_form = UserCreationForm


    fieldsets = (
        (None, {'fields': ('username', 'password', 'node')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
        ('Personal', {'fields': ('avatar',)}),
    )


