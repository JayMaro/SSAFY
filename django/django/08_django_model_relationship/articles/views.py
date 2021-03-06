from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_http_methods, require_POST
from django.http import HttpResponse, HttpResponseForbidden
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.core.paginator import Paginator

# Create your views here.
@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    paginator = Paginator(articles, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': articles,
        'page_obj': page_obj,
    }
    return render(request, 'articles/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@require_safe
def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


@require_POST
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_authenticated:
        if request.user == article.user:
            article.delete()
            return redirect('articles:index')
    return redirect('articles:detail', article.pk)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
        # return HttpResponseForbidden()
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)
        

@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
        return redirect('articles:detail', article.pk)
    return redirect('accounts:login')
    # return HttpResponse(status=401)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
        # return HttpResponseForbidden()
    return redirect('articles:detail', article_pk)
    # return HttpResponse(status=401)


@require_POST
def likes(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)

        if article.like_users.filter(pk=request.user.pk).exists():
        # if request.user in article.like_users.all():
            # ????????? ??????
            article.like_users.remove(request.user)
        else:
            # ????????? ??????
            article.like_users.add(request.user)
        return redirect('articles:index')
    return redirect('accounts:login')

"""
# [??????] ????????? ??????????????? ????????????
# https://docs.djangoproject.com/en/3.1/topics/db/queries/#querysets-are-lazy
# https://docs.djangoproject.com/en/3.1/ref/models/querysets/#when-querysets-are-evaluated
# https://docs.djangoproject.com/en/3.1/topics/db/queries/#caching-and-querysets

# ?????? ???????????? ????????? ???????????? DB ????????? ???????????? ?????? 
q = Entry.objects.filter(title__startswith="What")
q = q.filter(created_at__lte=datetime.date.today())
q = q.exclude(context__icontains="food")
print(q) # ????????? ?????? ???


# Iteration
# ???????????? ?????? ???????????? ?????? ????????? ??? ?????????????????? ????????? ??????(??????)
for e in Entry.objects.all():
    pass

# bool()
if Entry.objects.filter(title__'test'):
    pass


# ?????? ???
print([e.headline for e in Entry.objects.all()]) # ??????
print([e.pub_date for e in Entry.objects.all()]) # ??????

# ?????? ???
queryset = Entry.objects.all()
print([p.headline for p in queryset]) # Evaluate the query set. (??????)
print([p.pub_date for p in queryset]) # Re-use the cache from the evaluation. (???????????? ?????????)


# ?????? ???????????? ??????
queryset = Entry.objects.all()
print(queryset[5]) # Queries the database
print(queryset[5]) # Queries the database again

# ??? ????????? ???????????? ?????? ???
queryset = Entry.objects.all()
[entry for entry in queryset] # Queries the database (?????? ???????????? ?????? ????????????)
print(queryset[5]) # Uses cache
print(queryset[5]) # Uses cache



# ????????? LIKE ????????? ????????? ???????????????
like_set = article.like_users.filter(pk=request.user.pk)
if like_set: # ??????
    # ???????????? ?????? ????????? ???????????? ?????? ???????????????
    # ORM??? ?????? ????????? ?????????
    article.like_users.remove(request.user) 

# ?????? 1
# exists() ????????? ????????? ????????? ???????????? ?????? ???????????? ????????? ??????
if like_set.exists():
    # DB?????? ????????? ???????????? ?????????
    # ???????????? ????????? ??? ??????
    article.like_users.remove(request.user)


# ?????? IF ???????????? ???????????? ??????????

# if?????? ?????? ??? ??????
if like_set:
    # ??????????????? ????????? ????????? ???????????? ??????
    for user in like_set:
        print(user.username)


# ?????? ????????? ????????? ???????????? ???????????
# interator()
# ???????????? ?????? ???????????? ????????? ????????????, ?????? ????????? ???????????? ??????????????? ??????
# ?????? ???????????? ???????????? DB?????? ??????????????? ???????????? ??????
if like_set:
    for user in like_set.iterator():

# ????????? ???????????? ???????????? ????????? if ??????????????? ?????????
if like_set.exists():
    for user in like_set.iterator():
        pass
"""
