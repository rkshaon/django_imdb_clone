from django.db import models
from django.contrib.auth.models import User

from movie.models import Review

class Comment(models.Model):
    """docstring for Comment."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username) + ": " + str(self.body)
