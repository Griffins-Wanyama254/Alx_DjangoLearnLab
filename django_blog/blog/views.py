from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-published_date')[:5]
    return render(request, 'blog/index.html', {'posts': posts})
