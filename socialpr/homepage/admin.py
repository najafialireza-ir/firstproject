from django.contrib import admin
from .models import PostModel

@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created')
    search_fields = ('body', 'slug')
    list_filter = ('updated',) # filter by date 
    prepopulated_fields = {'slug':('body',)}