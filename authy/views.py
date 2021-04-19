from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator

from authy.forms import SignUpForm, ChangePasswordForm, EditProfileForm
from comment.forms import CommentForm
from authy.models import Profile
from movie.models import Movie, Review, Likes
from comment.models import Comment

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('form validation portion')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            return redirect('login')
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change-password-done')
    else:
        form = ChangePasswordForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'registration/change_password.html', context)

def password_change_done(request):
    return render(request, 'registration/change_password_done.html')

@login_required
def edit_profile(request):
    user = request.user.id
    profile = Profile.objects.get(user_id=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.picture = form.cleaned_data.get('picture')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('index')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'edit_profile.html', context)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    # profile movie data
    movie_watched_count = profile.watched.filter(Type='movie').count()
    series_watched_count = profile.watched.filter(Type='series').count()
    watch_list_count = profile.to_watch.all().count()
    movie_review_count = Review.objects.filter(user=user).count()

    context = {
        'profile': profile,
        'mWatched_count': movie_watched_count,
        'sWatched_count': series_watched_count,
        'watch_list_count': watch_list_count,
        'm_reviewd_count': movie_review_count,
    }

    template = loader.get_template('profile.html')

    return HttpResponse(template.render(context, request))

def user_watched_movies(request, username):
    user = get_object_or_404(User, username=username)
    profile =   Profile.objects.get(user=user)

    # profile movie data
    movie_watched_count = profile.watched.filter(Type='movie').count()
    series_watched_count = profile.watched.filter(Type='series').count()
    watch_list_count = profile.to_watch.all().count()
    movie_review_count = Review.objects.filter(user=user).count()

    # movie list
    movies = profile.watched.filter(Type='movie')
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'mWatched_count': movie_watched_count,
        'sWatched_count': series_watched_count,
        'watch_list_count': watch_list_count,
        'm_reviewd_count': movie_review_count,
        'movie_data': movie_data,
        'list_title': 'Movies Watched'
    }

    template = loader.get_template('profile.html')

    return HttpResponse(template.render(context, request))

def user_watched_series(request, username):
    user = get_object_or_404(User, username=username)
    profile =   Profile.objects.get(user=user)

    # profile movie data
    movie_watched_count = profile.watched.filter(Type='movie').count()
    series_watched_count = profile.watched.filter(Type='series').count()
    watch_list_count = profile.to_watch.all().count()
    movie_review_count = Review.objects.filter(user=user).count()

    # movie list
    movies = profile.watched.filter(Type='series')
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'mWatched_count': movie_watched_count,
        'sWatched_count': series_watched_count,
        'watch_list_count': watch_list_count,
        'm_reviewd_count': movie_review_count,
        'movie_data': movie_data,
        'list_title': 'Series Watched'
    }

    template = loader.get_template('profile.html')

    return HttpResponse(template.render(context, request))

def user_watch_list(request, username):
    user = get_object_or_404(User, username=username)
    profile =   Profile.objects.get(user=user)

    # profile movie data
    movie_watched_count = profile.watched.filter(Type='movie').count()
    series_watched_count = profile.watched.filter(Type='series').count()
    watch_list_count = profile.to_watch.all().count()
    movie_review_count = Review.objects.filter(user=user).count()

    # movie list
    movies = profile.to_watch.all()
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'mWatched_count': movie_watched_count,
        'sWatched_count': series_watched_count,
        'watch_list_count': watch_list_count,
        'm_reviewd_count': movie_review_count,
        'movie_data': movie_data,
        'list_title': 'Movie Watch List'
    }

    template = loader.get_template('profile.html')

    return HttpResponse(template.render(context, request))

def user_review_list(request, username):
    user = get_object_or_404(User, username=username)
    profile =   Profile.objects.get(user=user)

    # profile movie data
    movie_watched_count = profile.watched.filter(Type='movie').count()
    series_watched_count = profile.watched.filter(Type='series').count()
    watch_list_count = profile.to_watch.all().count()
    movie_review_count = Review.objects.filter(user=user).count()

    # movie list
    movies = Review.objects.filter(user=user)
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'mWatched_count': movie_watched_count,
        'sWatched_count': series_watched_count,
        'watch_list_count': watch_list_count,
        'm_reviewd_count': movie_review_count,
        'movie_data': movie_data,
        'list_title': 'Reviewed',
    }

    template = loader.get_template('profile.html')

    return HttpResponse(template.render(context, request))

def review_details(request, username, imdb_id):
    user_comment = request.user
    user = get_object_or_404(User, username=username)
    movie = Movie.objects.get(imdbID=imdb_id)
    review = Review.objects.get(user=user, movie=movie)

    comments = Comment.objects.filter(review=review).order_by('-date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = user_comment
            comment.save()
            return HttpResponseRedirect(reverse('review_details', args=[username, imdb_id]))
    else:
        form = CommentForm()

    context = {
        'review': review,
        'movie': movie,
        'comments': comments,
        'form': form,
    }

    template = loader.get_template('movie_review.html')

    return HttpResponse(template.render(context, request))

def like(request, username, imdb_id):
	user_liking = request.user
	user_review = get_object_or_404(User, username=username)
	movie = Movie.objects.get(imdbID=imdb_id)
	review = Review.objects.get(user=user_review, movie=movie)
	current_likes = review.likes

	liked = Likes.objects.filter(user=user_liking, review=review, type_like=2).count()

	if not liked:
		like = Likes.objects.create(user=user_liking, review=review, type_like=2)
		current_likes = current_likes + 1

	else:
		Likes.objects.filter(user=user_liking, review=review, type_like=2).delete()
		current_likes = current_likes - 1

	review.likes = current_likes
	review.save()

	return HttpResponseRedirect(reverse('review_details', args=[username, imdb_id]))

def unlike(request, username, imdb_id):
    user_unliking = request.user
    user_review = get_object_or_404(User, username=username)
    movie = Movie.objects.get(imdbID=imdb_id)
    review = Review.objects.get(user=user_review, movie=movie)
    current_unlikes = review.unlikes

    unliked = Likes.objects.filter(user=user_unliking, review=review, type_like=1).count()

    if not unliked:
        unlike = Likes.objects.create(user=user_unliking, review=review, type_like=2)
        current_unlikes = current_unlikes + 1
    else:
        Likes.objects.filter(user=user_unliking, review=review, type_like=2).delete()
        current_unlikes = current_unlikes + 1

    review.unlikes = current_unlikes
    review.save()

    return HttpResponseRedirect(reverse('review_details', args=[username, imdb_id]))
