from django.shortcuts import render, redirect
from django.http import HttpResponse
from onreview_app.models import Post, Comment
from onreview_app.forms import *

from django.shortcuts import render, render_to_response
import math
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from onreview.settings import LOGIN_URL, LOGOUT_URL

def list(request):
    posts = Post.objects.all()

    context = {
        'posts':posts.filter(active=True),
    }
    return render(request, 'list.html', context)

def post(request, id_parameter):
    id = int(id_parameter)
    post = Post.objects.get(pk=id)

    context = {
        'post':post,
        'active_comments':post.comments.filter(active=True)
    }
    return render(request, 'post.html', context)

def comment(request, id_parameter):
    id = int(id_parameter)
    comment = Comment.objects.get(pk=id)

    context = {
        'comment':comment,
    }
    return render(request, 'comment.html', context)

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

        form = CommentForm({'post_id':post_id, 'code':post.code})
        return render(request, 'add_comment_form.html', {'post': post, 'form':form})
    else:
        form = CommentForm(request.POST or None)
        if(form.is_valid()):
            print('valid')
            Comment.objects.create(
                    code=form.cleaned_data['code'],
                    description=form.cleaned_data['description'],
                    post=Post.objects.get(pk=form.cleaned_data['post_id']),
                    author=request.user
            )
            return redirect('/post/{}'.format(form.cleaned_data['post_id']), permanent=False)

        post = Post.objects.get(pk=form.cleaned_data['post_id'])
        return render(request, 'add_comment_form.html', {'post': post, 'form':form})
