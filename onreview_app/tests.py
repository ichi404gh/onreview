from django.test import TestCase
from django.contrib.auth.models import User
from onreview_app.models import *


class PostsAndCommentsTestCase(TestCase):
    user = None

    def setUp(self):
        self.user = User.objects.create_user(username='tester',
                                email='tester@tester.com',
                                password='testerpassword')

        Post.objects.create(author=User.objects.get(username="tester"),
                                                    code="#test.code()[]")

    def test_add_comment(self):
        p = self.user.posts.last()
        c = Comment.objects.create(post=p,author=self.user)
        c1 = Comment(author=self.user)
        self.assertEqual(p.comments.count(), 1)

        for c in p.comments.all():
            self.assertEqual(c.author.username,"tester")

    def test_comment_content(self):
        p = self.user.posts.last()
        c = Comment.objects.create(post=p, author=self.user,
                        code="#test.code()[1]", description="uncomment")
        self.assertEqual(p.comments.last().code, '#test.code()[1]')

    def test_diff_lines(self):
        p = self.user.posts.last()
        c = Comment.objects.create(post=p, author=self.user,
                        code="#test.code()[1]", description="uncomment")


        pdiff, cdiff = c.get_diff_lines()
        self.assertEqual(pdiff, [('eq','#test.code()[]')])
        self.assertEqual(cdiff, [('eq','#test.code()['),('mod','1'),('eq',']')])
