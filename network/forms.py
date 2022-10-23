from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)


class EditForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), required=True)
    id = forms.IntegerField(required=True, widget=forms.HiddenInput())


class LikeForm(forms.Form):
    id = forms.IntegerField(required=True, widget=forms.HiddenInput())
