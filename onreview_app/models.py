from django.db import models
from django.contrib.auth.models import User

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
    code = models.TextField('код', default=None, null=True)
    description = models.TextField('описание', default=None, null=True)

    def score(self):
        return self.scored_by.count()
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
