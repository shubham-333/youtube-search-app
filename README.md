# Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

# Basic Requirements:

- Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- A basic search API to search the stored videos using their title and description.
- Dockerize the project.
- It should be scalable and optimised.

#### :heavy_check_mark: | Make a dashboard to view the stored videos with filters and sorting options. 

# To Run Locally

* Clone the project
`git clone https://github.com/mogiiee/fp-youtube-api.git`

* Go to the project directory
`cd youtube_app`

* Set up a virtual environment for the project:
`python -m venv virtualenv`
`venv\source\activate`

* download redis from this [link](https://github.com/microsoftarchive/redis/releases)

* Install dependencies
`pip install requirements.txt`

* Modify settings.py File - add new YouTube Data API key at
`YOUTUBE_DATA_API_KEY`
  * For getting API keys follow [this](https://developers.google.com/youtube/v3/getting-started)

* To start the server, celery worker and celery beat, run the following commands in three seprate terminals
  * `python manage.py runserver`
  * `celery -A youtube_search.celery worker --pool=solo -l info` 
  * `celery -A youtube_search beat -l INFO`                      

* Go to the urls
  * http://localhost:8000/            # Youtube Home-Page with search feature
  * http://localhost:8000/viewlist/   # dashboard to view the stored videos with filters and sorting options

