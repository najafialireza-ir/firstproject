from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import PostModel, Relation
from django.contrib import messages
from .forms import PostForm, CommentForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils. decorators import method_decorator



class HomeView(View):
    def get(self, request):
        post = PostModel.objects.all()
        return render(request, 'homepage/home.html', {'posts':post})



class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = User.objects.get(pk=user_id)  # give user 
        post = user.puser.all() # use of realetd name and all()
        # post = PostModel.objects.filter(user=user)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'homepage/profile.html', {'user':user, 'posts':post,
                                                        'is_following':is_following})
    
    
    
class UserPostDetailView(LoginRequiredMixin, View):
    form_class = CommentForm
    
    
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(PostModel, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        comment = self.post_instance.pcomment.filter(is_reply=False)
        return render(request, 'homepage/detail.html', {'posts':self.post_instance, 'comments':comment,
                                                        'form':self.form_class})
    
    @method_decorator(login_required)
    def post(self, request, post_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Your Comment Sent', 'success')
            return redirect('home:post_detail', self.post_instance.id)
    

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(PostModel, pk=post_id)
        
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Your Post Deleted Successfully.', 'success')
        else:
            messages.error(request, "You can`t Deleted this message")
        return redirect('home:home')
    
    
class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostForm
    
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(PostModel, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'You can`t delete this post')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'homepage/update.html', {'form':form})
    
    
    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        
        if form.is_valid():
            new_post  = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:10])
            new_post.save()
            messages.success(request, 'Your Post Updated')
            return redirect('home:post_detail', new_post.id)
      

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'homepage/create.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Your New Post created', 'success')
            return redirect('home:post_detail', new_post.id)
        return render(request, 'homepage/create.html', {'form':form})
        
        
class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'You Already follow this user', 'danger')
            
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'Follow This User', 'success')
        return redirect('home:user_profile', user.id)
    
    
class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'User Unfollowed', 'success')
            
        else:
            messages.error(request, 'You don`t follow this user!')
        return redirect('home:user_profile', user.id)
    
    
