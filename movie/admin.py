from django.contrib import admin
from .models import *

admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(TodayClick)
admin.site.register(Evaluaton)

# Register your models here.
