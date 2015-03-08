from django.contrib.auth.admin import UserAdmin as BaseAdmin

class UserAdmin(BaseAdmin):
    
    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []
    
    list_display = ('username', 'date_joined', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
    )
    