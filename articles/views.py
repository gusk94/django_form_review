from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
# from IPython import embed

@require_GET
def index(request):
    # embed()
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


# accounts/login 이어서 별다른 설정없이 /accounts/login/ url로 이동
# @login_required(login_url='/accounts/login/')
@login_required
def create(request):
    if request.method == 'POST':
        # Article 생성해달라는 요청
        form = ArticleForm(request.POST)
        # embed()
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
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
    comments = article.comments.all()
    form = CommentForm()
    context = {'article': article, 'comments': comments, 'form': form}
    return render(request, 'articles/detail.html', context)


@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article_pk)
        else: # GET method
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:detail', article_pk)
    context = {'form': form}
    return render(request, 'articles/update.html', context)


@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if article.user == request.user:
            article.delete()
        else:
            return redirect('articles:detail', article_pk)
        # article.delete()
    return redirect('articles:index')


@require_POST
def commentcreate(request, article_pk):
    if request.user.is_authenticated:
    # article = get_object_or_404(Article, pk=article_pk)
    # content = request.POST.get('content') # name
    # comment = Comment()
    # comment.article = article
    # comment.content = content
    # comment.save()
        form = CommentForm(request.POST)
        if form.is_valid():
            # form.save()
            # article을 기본 form으로 받지 않고 exclude 했을 경우 article_id 를 따로 저장해줌
            comment = form.save(commit=False)
            comment.article_id = article_pk
            comment.user = request.user
            comment.save()
    return redirect('articles:detail', article_pk)


# @login_required
@require_POST
def commentdelete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
        return redirect('articles:detail', article_pk)
    else:
        return HttpResponse('You are Unauthorized', status=401)


def like(request, article_pk):
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)

    if article.liked_users.filter(pk=user.pk).exists(): # 1개의 데이터라도 존재하면 True
    # if user in article.liked_users.all():
        user.liked_articles.remove(article)
    else:
        user.liked_articles.add(article)

    return redirect('articles:detail', article_pk)


@login_required
def follow(request, article_pk, user_pk):
    # 로그인한 유저가 게시글 유저를 Follow or Unfollow 한다.
    # 로그인 유저
    user = request.user
    # 게시글 주인
    person = get_object_or_404(get_user_model(), pk=user_pk)

    if user in person.followers.all():
        # unfollow
        person.followers.remove(user) 
    else:
        # follow
        person.followers.add(user)
    return redirect('articles:detail', article_pk)