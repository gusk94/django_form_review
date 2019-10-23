from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        # fields = '__all__'
        fields = ['title', 'content', ]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # 리스트로 받고 싶은것만 받기 가능
        fields = '__all__'
        # 제외
        exclude = ['article', ]
