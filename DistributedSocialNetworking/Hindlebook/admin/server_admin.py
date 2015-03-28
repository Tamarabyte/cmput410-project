from django.contrib.admin import ModelAdmin

class NodeAdmin(ModelAdmin):

    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []

    list_display = ('host_name', 'get_primarykey', 'is_connected')
    ordering = ('host_name', )
    
    fieldsets = (
        (None, {'fields': ('host', 'team_number', 'is_connected')}),
        ('Basic Auth Incoming (From Them)', {'fields': ('host_name','password')}),
        ('Basic Auth Outgoing (To Them)', {'fields': ('our_username','our_password')}),
    )


    def get_primarykey(self, obj):
        return obj.pk
    get_primarykey.short_description = 'Primary Key'

class SettingsAdmin(ModelAdmin):

    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []

    list_display = ('node', 'connection_limit',)