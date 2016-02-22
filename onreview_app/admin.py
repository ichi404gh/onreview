from django.contrib import admin
from .models import *

class CommentInline(admin.TabularInline):
    model=Comment
    extra=0
    exclude = ('comment_diffs_internal', 'scored_by')

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date',)
    inlines=(CommentInline,)

admin.site.register(Post, PostAdmin)
