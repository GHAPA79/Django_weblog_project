from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date_modified',)
    ordering = ('status',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text', 'datetime_created')

# admin.site.register(Post, PostAdmin)
# admin.site.register(Comment, CommentAdmin)
