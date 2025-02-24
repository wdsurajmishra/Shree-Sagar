from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'view_count', 'get_like_count', 'get_comment_count')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Content', {
            'fields': ('content', 'description',)
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description')
        }),
        ('Thumbnail', {
            'fields': ('thumbnail',)
        }),
        ('Metadata', {
            'fields': ('view_count',)
        }),
    )

    

    actions = ['make_published', 'make_draft']

    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Mark selected posts as Published"


    def make_draft(self, request, queryset):
        queryset.update(status='draft')
    make_draft.short_description = "Mark selected posts as Draft"

    def get_like_count(self, obj):
        return obj.get_like_count()
    get_like_count.short_description = 'Likes'  # Label for the column

    # Define the method to display comment count
    def get_comment_count(self, obj):
        return obj.get_comment_count()
    get_comment_count.short_description = 'Comments'  


class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    list_filter = ['created_at', 'post__title']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    list_filter = ['created_at', 'post__title']

admin.site.register(Post, PostAdmin)    
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
