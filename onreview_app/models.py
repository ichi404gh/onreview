from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

class Post(models.Model):
    active = models.BooleanField(default=True)
    author = models.ForeignKey(
                        User,
                        related_name="posts")
    code = models.TextField('код')
    description = models.TextField('описание')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    scored_by = models.ManyToManyField(
                                User,
                                related_name='+',
                                blank=True)

    def score(self):
        return self.scored_by.count()

    def __str__(self):
        return "<{}>: {}".format(self.author.username, self.description[:20])

class Comment(models.Model):
    active = models.BooleanField(default=True)
    author = models.ForeignKey(User)
    post = models.ForeignKey(
                        Post,
                        default=None,
                        on_delete=models.CASCADE,
                        related_name="comments")

    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    scored_by = models.ManyToManyField(
                                User,
                                related_name='+',
                                blank=True)
    code = models.TextField('код', default="", blank=True)
    description = models.TextField('описание', default="", blank=True)
    comment_diffs_internal = models.TextField(default="", blank=True)

    def score(self):
        return self.scored_by.count()

    def get_diff(self):
        return json.loads(self.comment_diffs_internal)

    def get_diff_lines(self):
        import difflib

        postdiffs = list()
        commentdiffs = list()

        s = difflib.SequenceMatcher(lambda x: x.isspace(), self.post.code, self.code)
        for o in s.get_opcodes():
            if(o[0] in ('replace','delete')):
                postdiffs.append(('mod', s.a[o[1]:o[2]]))
            if(o[0] in ('replace','insert')):
                commentdiffs.append(('mod', s.b[o[3]:o[4]]))
            if(o[0] == 'equal'):
                postdiffs.append(('eq', s.a[o[1]:o[2]]))
                commentdiffs.append(('eq', s.b[o[3]:o[4]]))

            self.__normalize__(postdiffs)
            self.__normalize__(commentdiffs)
        return (postdiffs,commentdiffs)

    def __normalize__(self, array):
        if(len(array)==0):
            return
        i=0
        while(i<len(array)-1):
            if(array[i][0]==array[i+1][0]):
                d=(array[i][0], array[i][1]+array[i+1][1])
                del array[i+1]
                array[i]=d
            else:
                i+=1


@receiver(post_save, sender = Comment)
def parse_diffs(instance, **kwargs):
    # sender.save()
    comment = instance
    Comment.objects.filter(pk=instance.pk).update(
        comment_diffs_internal=json.dumps(comment.get_diff_lines())
    )
