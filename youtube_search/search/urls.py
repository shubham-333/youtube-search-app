from django.urls import path
from .import views

urlpatterns = [
    path('',views.index, name='index'),
    path('listview/',views.YoutubeItems.as_view(), name='test'),
]