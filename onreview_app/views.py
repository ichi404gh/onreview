from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Comment
from django.shortcuts import render
import math


def list(request):
    posts = Post.objects.all()

    context = {
        'posts':posts,
    }
    return render(request, 'list.html', context)

def post(request, id_parameter):
    id = int(id_parameter)
    post = Post.objects.get(pk=id)
    context = {
        'post':post,
    }

    return render(request, 'post.html', context)

def comment(request, id_parameter):
    id = int(id_parameter)
    comment = Comment.objects.get(pk=id)
    context = {
        'comment':comment,
    }

    return render(request, 'comment.html', context)
