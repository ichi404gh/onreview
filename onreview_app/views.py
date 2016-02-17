from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.shortcuts import render, render_to_response
import math


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

def add_post(request):
    if request.user.is_authenticated():
        if(request.method == 'GET'):
            return render(request, 'add_post_form.html')
        else:
            Post.objects.create(
                    author=request.user,
                    code=request.POST['code'],
                    description=request.POST['description']
            )

    return redirect('/', permanent=False)
