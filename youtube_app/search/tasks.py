# import django
# django.setup()
from django.conf import settings

import requests

from celery import shared_task
from isodate import parse_duration
from datetime import datetime
from .models import *

@shared_task(bind=True)
def update_data(self):
    videos = []

    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos' 
    search_params = {
        'part': 'snippet',
        'q': 'cricket',#request.POST['search'],
        'key': settings.YOUTUBE_DATA_API_KEY,
        'type' : 'video',
        'order' : 'date',
        'publishedAfter':'2020-01-01T00:00:00Z',
        'maxResults': 9,

    }
    
    r = requests.get(search_url, params=search_params)
    results = r.json()['items']


    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])
    
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
        # print(video_data['publishedAt'])
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

        videos.append(video_data)
    return 'Done'