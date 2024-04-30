from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='puser') # conection one to many
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    
    class Meta:
        # everywhere use PostModel get or post show by this ordering
        # if two post same u can use second item for show f.g ['created', 'body']
        ordering = ('-created',)
    

    def __str__(self):
        """show by those mehtods
        """
        return f'{self.user}-{self.body}'
    
    def get_absolute_url(self):
        """everywhere need this url u can call {{ post.get_absolute_url }}
        this method send url name and args.
        """
        return reverse('home:post_detail', args=(self.id,))
    
    def like_post(self):
        return self.pvote.count()
    
    def user_can_like(self, user):
        user_like = user.uvote.filter(post=self)
        if user_like.exists():
            return True # user liked this post
        return False  # user doesn`t like psot          
    
    
    
class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.form_user} following {self.to_user}'
    
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='pcomment')
    body = models.CharField(max_length=400)
    reply = models.ForeignKey('Comments', on_delete=models.CASCADE, related_name='rcomment', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.body}-{self.created}'
    
    
    
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvote')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='pvote')
    
    
    def __str__(self):
        return f'{self.user} liked {self.post.slug}'
    
