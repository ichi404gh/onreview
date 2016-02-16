from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
