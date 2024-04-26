from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import PostModel
from django.contrib import messages
from .forms import PostForm
from django.utils.text import slugify

class HomeView(View):
    def get(self, request):
        post = PostModel.objects.all()
        return render(request, 'homepage/home.html', {'posts':post})



class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)  # give user 
        post = PostModel.objects.filter(user=user)
        return render(request, 'homepage/profile.html', {'user':user, 'posts':post})
    
    
    
class UserPostDetailView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(PostModel, pk=post_id)
        return render(request, 'homepage/detail.html', {'posts':post})
    
    def post():
        pass
    

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
    # question
    
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
        