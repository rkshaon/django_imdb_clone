from django.urls import path
from movie.views import index, pagination, movie_details

urlpatterns = [
    path('', index, name='index'),
    path('search/<query>/page/<page_number>', pagination, name='pagination'),
    path('<imdb_id>', movie_details, name='movie-details'),
]
