from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import View, ListView, DetailView
from .models import *
from .forms import *
from django.db.models import Q
import math
import requests
from bs4 import BeautifulSoup
from django.db.models import Count
import datetime
from .models import *



class Main(ListView):
    model = Movie
    template_name = 'movie/main.html'

def search_list(request):

    search_key = request.GET.get('search_key', None)

    search_key = search_key.replace(" ", "")
    space = '\s*'
    re_search_key = space.join(search_key)

    if search_key:
        movies = Movie.objects.filter(subject__iregex=re_search_key)

        if not movies:
            print('db없음 확인')
            custom_header = {
                'referer': 'https://www.netflix.com/browse',
                'useragent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            }


            url = f'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=영화 {search_key}'
            print(url)
            r = requests.get(url, headers=custom_header)
            if r.status_code == requests.codes.ok:
                print('접속성공')
                html = BeautifulSoup(r.text, 'html.parser')
                is_movie = html.select('div.movie_info div.section_head h2')
                print(is_movie)

                if is_movie and is_movie[0].text == '네이버 영화':
                    return save_db(html, request)

                else:
                    #
                    # q1 = Q(created__gte=datetime.date.today())
                    # q2 = Q(created__lte=datetime.date.today() + datetime.timedelta(days=1))
                    #
                    # # 문제의 부분
                    # top_movies = TodayClick.objects.\
                    #                  filter(q1, q2).annotate(count=Count('movie')).order_by('-count')[:5]
                    #
                    # # 이 방법이 아닌걸까요
                    top_movies = []
                    message = '검색결과가 없습니다.'
                    return render(request, 'movie/search_list.html', {'object_list': top_movies, 'message': message})

    else:
        movies = get_list_or_404(Movie)

    return render(request, 'movie/search_list.html', {'object_list': movies})


def save_db(html, request):
    subject = html.select('div.movie_info div.info_main h3 ')[0].text.split(',')[0] + ')'
    poster = html.select_one('div.movie_info div.thumb img').attrs['src']
    director = html.select_one('dl.desc_detail a').text
    documents = [Movie.objects.create(subject=subject, poster=poster, director=director)]
    return render(request, 'movie/search_list.html', {'object_list': documents})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.GET.get('eval'):
        point = int(request.GET.get('eval')[0])
        user = request.user
        movie.evaluate.create(point=point, user=user)

    sum = 0
    evaluations = movie.evaluate.all()
    for evaluation in evaluations:
        sum += int(evaluation.point)

    if sum != 0:
        average = round(sum/len(evaluations),2)
    else:
        average = 0

    movie.todayclick.create()

    if request.method == "POST":
        comments_form = CommentForm(request.POST)
        comments_form.instance.author_id = request.user.id
        comments_form.instance.movie_id = movie_id
        if comments_form.is_valid():
            comments_form.save()

    comments_form = CommentForm()
    comments = movie.comments.all()

    return render(request, 'movie/movie_detail.html',\
                  {'object':movie, 'comments':comments, 'comments_form':comments_form, 'average':average})

def evaluate(request):
    print(request.GET)
    return render(request, 'movie/main.html')





def test(request):

    return render(request, 'movie/cal.html')
