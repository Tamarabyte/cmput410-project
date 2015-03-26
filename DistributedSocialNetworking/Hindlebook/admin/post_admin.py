from django.contrib.admin import ModelAdmin, TabularInline
from Hindlebook.models import Comment, Image

class ImagesAdmin(TabularInline):
    model = Image
    extra = 0

class CommentsAdmin(TabularInline):
    model = Comment
    ordering = ("-pubDate",)
    extra = 0

class PostAdmin(ModelAdmin):

    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []

    list_display = ('pubDate', 'get_authorname', 'guid')
    ordering = ("-pubDate",)

    inlines = [ImagesAdmin, CommentsAdmin]
    filter_horizontal = ('categories',)


    fieldsets = (
        (None, {'fields': ('author', 'visibility')}),
        ('Post', {'fields': ('title', 'description', 'content', 'categories')}),
        ('Server Details', {'fields': ('guid', 'origin', 'source')}),
    )



    def get_authorname(self, obj):
        return obj.author.username
    get_authorname.short_description = 'Author'

class CategoryAdmin(ModelAdmin):

    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []

    list_display = ('tag',)