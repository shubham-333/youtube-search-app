from django.conf import settings
from django.shortcuts import render, redirect
import requests
from isodate import parse_duration
from datetime import datetime

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
            'maxResults': 100,

        }
        
        r = requests.get(search_url, params=search_params)
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
                'publishedAt': datetime.strptime(result['snippet']['publishedAt'],'%Y-%m-%dT%H:%M:%SZ').strftime('%d %b, %Y'),
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
            }
            print(video_data['publishedAt'])

            videos.append(video_data)

    context = {
        'videos' : videos
    }


    return render(request, 'search/index.html', context)
