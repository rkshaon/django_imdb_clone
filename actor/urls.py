from django.urls import path
from actor.views import actors

urlpatterns = [
    path('<slug:actor_slug>', actors, name='actors'),
]
