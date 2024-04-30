from django import forms
from .models import PostModel, Comments



class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('body',)
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs={'class':'form-control'})
        }
        
        
class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body', )
        

class SearchPostForm(forms.Form):
    search = forms.CharField()