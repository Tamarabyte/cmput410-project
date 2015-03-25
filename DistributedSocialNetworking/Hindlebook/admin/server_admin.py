from django.contrib.admin import ModelAdmin

class NodeAdmin(ModelAdmin):

    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []

    list_display = ('host_name', 'host', 'get_primarykey')
    ordering = ('host_name', )


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