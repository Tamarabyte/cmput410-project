from django.contrib.admin import ModelAdmin

class NodeAdmin(ModelAdmin):

    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []

    list_display = ('host_name', 'host')
    ordering = ('host_name', )


class ServerAdmin(ModelAdmin):

    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []

    list_display = ('id', 'host_name', 'host')