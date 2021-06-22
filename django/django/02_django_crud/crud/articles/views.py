from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def index(request):
    # 모든 게시글을 조회

    # 1. DB로부터 받은 쿼리셋을 이후에 파이썬이 정렬 변경 (python이 조작)
    # articles = Article.objects.all()[::-1]

    # 2. 처음부터 원하는 정렬로 된 쿼리셋을 받음 (DB가 조작)
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


def new(request):
    return render(request, 'articles/new.html')


def create(request):
    # 1. new로 부터 받은 데이터를 저장
    title = request.POST.get('title')
    content = request.POST.get('content')

    # 2. 저장한 데이터를 DB에 저장
    # 2-1
    # article = Article()
    # article.title = title
    # article.content = content
    # article.save()

    # 2-2
    article = Article(title=title, content=content)
    article.save()

    # 2-3
    # Article.objects.create(title=title, content=content)

    # return redirect('/articles/index/')
    # return redirect(f'/articles/{article.pk}/')
    return redirect('articles:detail', article.pk)


def detail(request, pk):
    # 몇번 글을 조회할건지 가져와야 함
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


def delete(request, pk):
    # 삭제할 게시글 조회
    article = Article.objects.get(pk=pk)
    # 삭제 요청이 POST면 삭제, POST가 아니라면 DETAIL 페이지로 redirect
    if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    else:
        return redirect('articles:detail', article.pk)


def edit(request, pk):
    # 수정할 게시글 조회
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/edit.html', context)


def update(request, pk):
    # 수정될 게시글 조회
    article = Article.objects.get(pk=pk)

    # edit으로부터 수정되는 데이터 받아서 수정 진행
    article.title = request.POST.get('title')
    article.content = request.POST.get('content')
    article.save()

    return redirect('articles:detail', article.pk)
