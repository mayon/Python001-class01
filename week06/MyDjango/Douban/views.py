from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Comment

# Create your views here.

def comment(request):
  shorts = Comment.objects.filter(votes__gt=30)
  return render(request, 'result.html', locals())
