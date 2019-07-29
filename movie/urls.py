
from django.urls import path
from .views import *

app_name = 'movie'

urlpatterns = [
    path('evaluate/', evaluate, name='evaluate'),
    path('test/', test, name='test'),
    path('search_list/', search_list, name='search_list'),
    path('detail/<int:movie_id>/', movie_detail, name='detail'),
    path('', Main.as_view(), name='index'),
]
