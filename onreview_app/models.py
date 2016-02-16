from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    active = models.BooleanField(default=True)
    author = models.ForeignKey(User)
    code = models.TextField('код')
    description = models.TextField('описание')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    scored_by = models.ManyToManyField(
                                User,
                                related_name='+',
                                blank=True)

    def score(self):
        return self.scored_by.count()

class Comment(models.Model):
    active = models.BooleanField(default=True)
    author = models.ForeignKey(User)
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    scored_by = models.ManyToManyField(
                                User,
                                related_name='+',
                                blank=True)
    def score(self):
        return self.scored_by.count()
