from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)


class EditPostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), required=True)
    id = forms.IntegerField(required=True, widget=forms.HiddenInput())


class EditCommForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), required=True)
    post_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    comment_id = forms.IntegerField(required=True, widget=forms.HiddenInput())


class LikeForm(forms.Form):
    id = forms.IntegerField(required=True, widget=forms.HiddenInput())


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class FollowForm(forms.Form):
    id = forms.IntegerField(required=True, widget=forms.HiddenInput())
