from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.utils.text import slugify
from django.core.paginator import Paginator
import requests
from django.contrib.auth.models import User

from movie.models import Movie, Genre, Rating, Review
from actor.models import Actor
from authy.models import Profile
from movie.forms import RateForm

def index(request):
    query = request.GET.get('q')

    if query:
        url = 'http://www.omdbapi.com/?apikey=ecd537eb&s=' + query
        response = requests.get(url)
        movie_data = response.json()

        context = {
            'query': query,
            'movie_data': movie_data,
            'page_number': 1,
        }
        template = loader.get_template('search_result.html')
        return HttpResponse(template.render(context, request))

    return render(request, 'index.html')

def pagination(request, query, page_number):
    url = 'http://www.omdbapi.com/?apikey=ecd537eb&s=' + query + '&page=' + str(page_number)
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) + 1
    context = {
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number,
    }
    template = loader.get_template('search_result.html')
    return HttpResponse(template.render(context, request))

def movie_details(request, imdb_id):
    if Movie.objects.filter(imdbID=imdb_id).exists():
        movie_data = Movie.objects.get(imdbID=imdb_id)
        reviews = Review.objects.filter(movie=movie_data)
        reviews_avg = reviews.aggregate(Avg('rate'))
        reviews_count = reviews.count()
        our_db = True
    else:
        url = 'http://www.omdbapi.com/?apikey=ecd537eb&i=' + imdb_id
        response = requests.get(url)
        movie_data = response.json()

        # Inject to Our Database
        rating_objs = []
        genre_objs = []
        actor_objs = []

        # For actors
        actor_list = [x.strip() for x in movie_data['Actors'].split(',')]

        for actor in actor_list:
            a, created = Actor.objects.get_or_create(name=actor)
            actor_objs.append(a)

        # For genres
        genre_list = list(movie_data['Genre'].replace(" ", "").split(','))

        for genre in genre_list:
            genre_slug = slugify(genre)
            g, created = Genre.objects.get_or_create(title=genre, slug=genre_slug)
            genre_objs.append(g)

        # For ratings
        for rate in movie_data['Ratings']:
            r, created = Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
            rating_objs.append(r)

        if movie_data['Type'] == 'movie':
            m, created = Movie.objects.get_or_create(
                Title = movie_data['Title'],
                Year = movie_data['Year'],
                Rated = movie_data['Rated'],
                Released = movie_data['Released'],
                Runtime = movie_data['Runtime'],
                Director = movie_data['Director'],
                Writer = movie_data['Writer'],
                Plot = movie_data['Plot'],
                Language = movie_data['Language'],
                Country = movie_data['Country'],
                Awards = movie_data['Awards'],
                Poster_url = movie_data['Poster'],
                Metascore = movie_data['Metascore'],
                imdbRating = movie_data['imdbRating'],
                imdbVotes = movie_data['imdbVotes'],
                imdbID = movie_data['imdbID'],
                Type = movie_data['Type'],
                DVD = movie_data['DVD'],
                BoxOffice = movie_data['BoxOffice'],
                Production = movie_data['Production'],
                Website = movie_data['Website'],
            )
            m.Genre.set(genre_objs)
            m.Actors.set(actor_objs)
            m.Ratings.set(rating_objs)
        else:
            m, created = Movie.objects.get_or_create(
                Title = movie_data['Title'],
                Year = movie_data['Year'],
                Rated = movie_data['Rated'],
                Released = movie_data['Released'],
                Runtime = movie_data['Runtime'],
                Director = movie_data['Director'],
                Writer = movie_data['Writer'],
                Plot = movie_data['Plot'],
                Language = movie_data['Language'],
                Country = movie_data['Country'],
                Awards = movie_data['Awards'],
                Poster_url = movie_data['Poster'],
                Metascore = movie_data['Metascore'],
                imdbRating = movie_data['imdbRating'],
                imdbVotes = movie_data['imdbVotes'],
                imdbID = movie_data['imdbID'],
                Type = movie_data['Type'],
                totalSeasons = movie_data['totalSeasons'],
            )
            m.Genre.set(genre_objs)
            m.Actors.set(actor_objs)
            m.Ratings.set(rating_objs)

        for actor in actor_objs:
            actor.movies.add(m)
            actor.save()

        m.save()
        our_db = False

    context = {
        'movie_data': movie_data,        
        'reviews': reviews,
        'reviews_avg': reviews_avg,
        'reviews_count': reviews_count,
        'our_db': our_db,
    }

    template = loader.get_template('movie_details.html')
    return HttpResponse(template.render(context, request))

def genres(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    movies = Movie.objects.filter(Genre=genre)
    # Pagination
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)
    context = {
        'movie_data': movie_data,
        'genre': genre
    }
    template = loader.get_template('genre.html')
    return HttpResponse(template.render(context, request))

def add_movie_to_watch(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    profile.to_watch.add(movie)

    return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))

def add_movie_to_watched(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if profile.to_watch.filter(imdbID=imdb_id).exists():
        profile.to_watch.remove(movie)

    profile.watched.add(movie)

    return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))

def rate(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user
            rate.movie = movie
            rate.save()
            return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))
    else:
        form = RateForm()

    context = {
        'form': form,
        'movie': movie,
    }

    template = loader.get_template('rate.html')
    return HttpResponse(template.render(context, request))

def
