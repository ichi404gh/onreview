from django.shortcuts import render, redirect
from django.http import HttpResponse
from onreview_app.models import Post, Comment
from onreview_app.forms import *

from django.shortcuts import render, render_to_response
import math
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from onreview.settings import LOGIN_URL, LOGOUT_URL

def list(request):
    posts = Post.objects.all()

    context = {
        'posts':posts.filter(active=True).order_by('-pub_date'),
    }
    return render(request, 'list.html', context)

def post(request, id_parameter):
    post = Post.objects.get(pk=id_parameter)

    context = {
        'post':post,
        'active_comments':post.comments.filter(active=True)\
                    .annotate(score=Count('scored_by'))\
                    .order_by('-score', 'pub_date'),
        'scored': request.user in post.scored_by.all()
    }
    return render(request, 'post.html', context)

def comment(request, id_parameter):
    comment = Comment.objects.get(pk=id_parameter)

    context = {
        'comment':comment,
        'scored': request.user in comment.scored_by.all()
    }
    return render(request, 'comment.html', context)

def vote(obj, user):
    if(user in obj.scored_by.all()):
        obj.scored_by.remove(user)
    else:
        obj.scored_by.add(user)

@login_required
def vote_post(request, id_parameter):
    obj = Post.objects.get(pk=id_parameter)
    vote(obj, request.user)
    return redirect('/post/{}'.format(id_parameter), permanent=False)

@login_required
def vote_comment(request, id_parameter):
    obj = Comment.objects.get(pk=id_parameter)
    vote(obj, request.user)
    return redirect('/comment/{}'.format(id_parameter), permanent=False)


@login_required
def add_post(request):
        if(request.method == 'GET'):
            return render(request, 'add_post_form.html')
        else:
            Post.objects.create(
                    author=request.user,
                    code=request.POST['code'],
                    description=request.POST['description']
            )
            return redirect('/', permanent=False)

@login_required
def add_comment(request, post_id):
    if(request.method == 'GET'):
        post = Post.objects.get(pk=post_id)
        form = CommentForm({'post_id':post.id, 'code':post.code})
        return render(request, 'add_comment_form.html', {'post': post, 'form':form})
    else:
        form = CommentForm(request.POST or None)
        if(form.is_valid()):
            Comment.objects.create(
                    code=form.cleaned_data['code'],
                    description=form.cleaned_data['description'],
                    post=Post.objects.get(pk=form.cleaned_data['post_id']),
                    author=request.user
            )
            return redirect('/post/{}'.format(form.cleaned_data['post_id']), permanent=False)

        post = Post.objects.get(pk=form.cleaned_data['post_id'])
        return render(request, 'add_comment_form.html', {'post': post, 'form':form})
