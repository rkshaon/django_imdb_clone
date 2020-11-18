from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from actor.models import Actor
from movie.models import Movie

def actors(request, actor_slug):
    actor = get_object_or_404(Actor, slug=actor_slug)
    movies = Movie.objects.filter(Actors=actor)

    # Pagination
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'actor': actor,
    }

    template = loader.get_template('actor.html')
    return HttpResponse(template.render(context, request))
