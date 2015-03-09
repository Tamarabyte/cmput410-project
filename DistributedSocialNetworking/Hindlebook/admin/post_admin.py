from django.contrib.admin import ModelAdmin, TabularInline
from Hindlebook.models import Comment, Image

class ImagesAdmin(TabularInline):
    model = Image
    extra = 0

class CommentsAdmin(TabularInline):
    model = Comment
    ordering = ("-pub_date",)
    extra = 0


class PostAdmin(ModelAdmin):

    # List View Attributes
    list_filter = []
    search_fields = []
    exclude = []
    inlines = []

    list_display = ('pub_date', 'get_authorname', 'uuid')
    ordering = ("-pub_date",)

    inlines = [ImagesAdmin, CommentsAdmin]


    fieldsets = (
        (None, {'fields': ('author', 'privacy')}),
        ('Post', {'fields': ('title', 'description', 'text')}),
        ('Server Details', {'fields': ('uuid',)}),
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