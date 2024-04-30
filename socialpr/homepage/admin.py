from django.contrib import admin
from .models import PostModel, Relation, Comments, Vote



@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created')
    search_fields = ('body', 'slug')
    list_filter = ('updated',) # filter by date 
    prepopulated_fields = {'slug':('body',)}
    
    
admin.site.register(Relation)


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'is_reply')
    search_fields = ('body', 'reply')
    list_filter = ('created',)
    
    
    
admin.site.register(Vote)