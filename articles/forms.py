from django import forms
from .models import Comment, Article, ArticleImage
from ckeditor.widgets import CKEditorWidget
from django.forms import modelformset_factory

# Kommentariya formasi
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': "Kommentariya yozing...",
                'class': 'form-control',
            }),
        }

# Asosiy maqola formasi
class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(), label='Maqola matni')

    class Meta:
        model = Article
        fields = ['title', 'summary', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sarlavha'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Qisqacha mazmuni'}),
        }

class ArticleImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = ArticleImage
        fields = ['image']


# Rasmlar formasi to‘plami (modelformset)
ImageFormSet = modelformset_factory(
    ArticleImage,
    form=ArticleImageForm,
    extra=5,
    max_num=5,
    validate_max=True,
    can_delete=True
)
