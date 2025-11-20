from django.shortcuts import render
from .models import blogPost
# Create your views here.
from django.http import HttpResponse

def index(request):
    blogs = blogPost.objects.all()
    print(blogs)
    allBlogs = []
    n  = len(blogs)
    allBlogs.append([blogs, n])
    print(allBlogs)
    params = {'allBlogs': allBlogs}
    return render(request, 'blog/index.html', params)

def blogpost(request, id):
    blog = blogPost.objects.filter(blog_id = id)[0]
    print(blog)
    return render(request, 'blog/blogpost.html',{'blog':blog})
