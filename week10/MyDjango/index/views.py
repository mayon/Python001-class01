from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import time

from .models import Comment
from django.db.models import Avg, Sum, Max, Min, Count

# Create your views here.

def index(request):
    all_comments = Comment.objects.all()

    goods_sum = all_comments.values('goods_title').annotate(c=Count('goods_title')).count()
    comments_sum = all_comments.count()
    sentiment = all_comments.aggregate(Avg("sentiment"))['sentiment__avg']
    sentiment_large = all_comments.filter(sentiment__gte=0.5).count()
    sentiment_small = comments_sum - sentiment_large

    goodss = all_comments.values('goods_title', 'goods_author').annotate(comment_count=Count('goods_title'), goods_sentiment=Avg('sentiment')).order_by('-goods_sentiment')
    comments = all_comments.order_by('-sentiment')[:10]
    return render(request, 'index.html', locals())

class CommentView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET
        comments = Comment.objects.order_by('comment_time')
        if 'time_type' in query.keys() and query['time_type'] == 'created_time':
            if query['from']:
                comments = comments.filter(created_time__gte=(query['from'] + ' 00:00'))
            if query['to']:
                comments = comments.filter(created_time__lte=(query['to'] + ' 23:59'))
        elif 'time_type' in query.keys() and query['time_type'] == 'comment_time':
            if query['from']:
                comments = comments.filter(comment_time__gte=(query['from'] + ' 00:00'))
            if query['to']:
                comments = comments.filter(comment_time__lte=(query['to'] + ' 23:59'))
        if 'keyword' in query.keys() and query['keyword']:
            comments = comments.filter(content__contains=query['keyword']) 
        return render(request, 'comment.html', locals())