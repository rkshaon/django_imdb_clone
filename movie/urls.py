from django.urls import path
from movie.views import index

urlpatterns = [
    path('', index, name='index'),
]
