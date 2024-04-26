from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='puser') # conection one to many
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        """show by those mehtods
        """
        return f'{self.user}-{self.body}'
    
    def get_absolute_url(self):
        """everywhere need this url u can call {{ post.get_absolute_url }}
        this method send url name and args.
        """
        return reverse('home:post_detail', args=(self.id,))
    