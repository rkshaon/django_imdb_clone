from django.urls import path
from movie.views import index, pagination, movie_details, genres, add_movie_to_watch, add_movie_to_watched

urlpatterns = [
    path('', index, name='index'),
    path('search/<query>/page/<page_number>', pagination, name='pagination'),
    path('<imdb_id>', movie_details, name='movie-details'),
    path('<imdb_id>/addmovietowatch', add_movie_to_watch, name='add_movie_to_watch'),
    path('<imdb_id>/addmovietowatched', add_movie_to_watched, name='add_movie_to_watched'),
    path('genre/<slug:genre_slug>', genres, name='genres'),
]
