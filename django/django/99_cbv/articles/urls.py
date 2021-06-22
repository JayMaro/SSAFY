from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import (AboutView, 
                    IndexView, 
                    ArticleListView, 
                    ArticleDetailView,
                    ArticleCreateView,
                    ArticleUpdateView,
                    ArticleDeleteView,
)

app_name = 'articles'

urlpatterns = [
    path('about/', TemplateView.as_view(template_name="articles/about.html")),
    path('about2/', views.about2),
    path('about3/', AboutView.as_view()),
    path('index/', views.index),
    path('index2/', IndexView.as_view()),
    # --
    path('', ArticleListView.as_view(), name='index'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='detail'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete'),
]
