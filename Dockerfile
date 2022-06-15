FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver",,"0.0.0.8000"]

# commands
# docker build --tag youtube_app .
# docker run -p 8000:8000 youtube_app