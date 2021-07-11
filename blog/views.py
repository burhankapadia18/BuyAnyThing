from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost


# Create your views here.

def index(request):
    posts = Blogpost.objects.all()
    print(posts)
    return render(request, "blog/index.html", {'posts': posts})


def blogpost(request, pid):
    # fetch the post using id
    post = Blogpost.objects.filter(post_id=pid)
    return render(request, "blog/blogpost.html", {'post': post[0]})
