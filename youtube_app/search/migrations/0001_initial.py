# Generated by Django 4.0.5 on 2022-06-15 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(max_length=200)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=5000, null=True)),
                ('publishedDateTime', models.DateTimeField()),
                ('thumbnailsUrls', models.URLField()),
                ('channel_id', models.CharField(max_length=500)),
                ('channel_title', models.CharField(blank=True, max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]