from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Movie
from django.core.paginator import Paginator
from django.core import serializers
from django.http.response import HttpResponse

# Create your views here.
@require_GET
def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)

    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    if request.is_ajax():
        data = serializers.serialize('json', movies)
        return HttpResponse(data, content_type='application/json')
    else:
        context = {
            'movies': movies,
        }
        return render(request, 'movies/index_vue.html', context)


@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)


@require_GET
def recommended(request):
    pass
