from django.shortcuts import render

from django.conf import settings
from django.shortcuts import render, redirect
import requests
from isodate import parse_duration
from datetime import datetime
from django.http import HttpResponse

from .models import *
# from .tasks import test_func

# def test(request):
#     test_func.delay()
#     return HttpResponse("Done")
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

# Rest FrameWork
from rest_framework import generics
from rest_framework.pagination import CursorPagination

class ResultsPagination(CursorPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

# Searching is implemented using DRF Filters
# DRF filter by default uses [icontains] and thus the search by default supports partial searches

class YoutubeItems(generics.ListAPIView):
    search_fields = ['title', 'description']
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter)
    filterset_fields = ['channel_id','channel_title']
    ordering = ('-publishedDateTime')
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer
    pagination_class = ResultsPagination


def index(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos' 
        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'type' : 'video',
            'order' : 'date',
            'publishedAfter':'2020-01-01T00:00:00Z',
            'maxResults': 9,

        }
        
        r = requests.get(search_url, params=search_params)
        print(r.json())
        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')
        
        video_params = {
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']
        videos = []

        
        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'publishedDateTime':result['snippet']['publishedAt'],
                'publishedAt': datetime.strptime(result['snippet']['publishedAt'],'%Y-%m-%dT%H:%M:%SZ').strftime('%d %b, %Y'),
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
                'description': result['snippet']['description'],
            }
            print(video_data['publishedAt'])

            videos.append(video_data)
            Videos.objects.create(
                    video_id=video_data['id'],
                    title=video_data['title'],
                    description=video_data['description'],
                    # channel_id=channel_id,
                    # channel_title=channel_title,
                    publishedDateTime=video_data['publishedDateTime'],
                    # thumbnailUrl=video_data['thumbnail'],
                    # videoUrl=video_data['url'],
                )

    context = {
        'videos' : videos
    }


    return render(request, 'search/index.html', context)
