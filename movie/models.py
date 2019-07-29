from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    subject = models.CharField(max_length=50)
    director = models.CharField(max_length=50, blank=True)
    poster = models.TextField(blank=True, null=True)
    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='Movie')
    description = models.CharField(max_length=1000, blank=True)
    click = models.IntegerField(default=0)

    def __str__(self):
        return self.subject

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')

class TodayClick(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='todayclick')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.movie)

class Evaluaton(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='evaluate')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='evaluation')
    point = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)+'_'+str(self.movie)
