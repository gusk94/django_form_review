from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from .forms import ArticleForm
from .models import Article
# from IPython import embed

@require_GET
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


def create(request):
    if request.method == 'POST':
        # Article 생성해달라는 요청
        form = ArticleForm(request.POST)
        # embed()
        if form.is_valid():
            form.save()
            return redirect('articles:index')
        # else:
        #     context = {'form': form}
        #     return render(request, 'articles/create.html', context)
    else: # GET
        # Article 생성하기 위한 페이지 요청
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)


@require_GET
def detail(request, article_pk):
    # 사용자가 url 에 적어보낸 article pk 를 통해서 디테일 페이지를 보여준다.
    article = get_object_or_404(Article, pk=article_pk)
    context = {'article': article}
    return render(request, 'articles/detail.html', context)


def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_pk)
    else:
        form = ArticleForm(instance=article)
    context = {'form': form}
    return render(request, 'articles/update.html', context)


@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect('articles:index')