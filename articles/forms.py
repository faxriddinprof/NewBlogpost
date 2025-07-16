from django import forms
from .models import Comment
from .models import Article
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "Kommentariya yozing..."}),
        }

class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = ['title', 'summary', 'body', 'photo']
        widgets = {
            'body': CKEditorWidget(),
        }   