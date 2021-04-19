from django.contrib import admin
from .models import Genre, Rating, Movie, Review, Likes

admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Likes)
