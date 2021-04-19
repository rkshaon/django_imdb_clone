"""imdb_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from authy.views import user_profile, review_details, like, unlike, user_watched_movies, user_watched_series, user_watch_list, user_review_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('actor/', include('actor.urls')),
    path('account/', include('authy.urls')),
    path('<username>/', user_profile, name='user_profile'),
    path('<username>/watched-movies', user_watched_movies, name='user_watched_movies'),
    path('<username>/watched-series', user_watched_series, name='user_watched_series'),
    path('<username>/watch-list', user_watch_list, name='user_watch_list'),
    path('<username>/reviewed', user_review_list, name='user_review_list'),
    path('<username>/review/<imdb_id>', review_details, name='review_details'),
    path('<username>/review/<imdb_id>/like', like, name='review_like'),
    path('<username>/review/<imdb_id>/unlike', unlike, name='review_unlike'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
